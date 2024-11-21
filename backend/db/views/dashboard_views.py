from django.utils import timezone  # Added for dashboard (net calcs)
from datetime import timedelta  # Added for forecasting and dashboard (net calcs)
from django.db.models import Sum, F, Q  # Added for forecasting and dashboard (net calcs & breakdown)
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from ..models import Inventory, Dashboard, InventoryHistory, SalesOrderShipment, PurchaseOrder
from ..serializers import DashboardSerializer

# --- Constants for time frames --- #

TIME_FRAMES = {
    '24h': timedelta(hours=24),
    'week': timedelta(weeks=1),
    'month': timedelta(days=30),
}


# --- Transaction types --- #

TRANSACTION_TYPES = {
    'sale': 'sale',
    'restock': 'restock',
}


# --------- HELPER FUNCTIONS --------- #

# Return the start and end dates based on the time frame or custom inputs.
def get_time_frame_range(time_frame, custom_start=None, custom_end=None):
    if custom_start and custom_end:
        return (
            timezone.datetime.strptime(custom_start, '%Y-%m-%d').date(),
            timezone.datetime.strptime(custom_end, '%Y-%m-%d').date()
        )
    if time_frame in TIME_FRAMES:
        start_date = timezone.now() - TIME_FRAMES[time_frame]
        return start_date, None
    if time_frame == 'overall':
        return None, None
    raise ValueError("Invalid time frame")

# Filter InventoryHistory based on transaction type and date range.
def query_inventory_history(transaction_type, start_date=None, end_date=None):
    query = InventoryHistory.objects.filter(transaction_type=transaction_type)
    if start_date:
        query = query.filter(transaction_date__gte=start_date)
    if end_date:
        query = query.filter(transaction_date__lte=end_date)
    return query

# Calculate aggregates like total price or quantity for a queryset.
def calculate_aggregates(queryset, fields):
    return queryset.aggregate(**fields)


# --------- DASHBOARD VIEWS --------- #

# List dashboard data or add a new dashboard item
@api_view(['GET', 'POST'])
def dashboard_list(request):
    if request.method == 'GET':
        # Retrieve all dashboard data
        dashboards = Dashboard.objects.filter(is_deleted=False)  # Exclude soft-deleted items
        serializer = DashboardSerializer(dashboards, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        # Add a new dashboard entry
        serializer = DashboardSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Retrieve, update, or soft-delete a specific dashboard entry
@api_view(['GET', 'PUT', 'DELETE'])
def dashboard_detail(request, pk):
    try:
        dashboard = Dashboard.objects.get(pk=pk, is_deleted=False)
    except Dashboard.DoesNotExist:
        return Response({'error': 'Dashboard not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        # Return dashboard data
        serializer = DashboardSerializer(dashboard)
        return Response(serializer.data)

    elif request.method == 'PUT':
        # Update dashboard data
        serializer = DashboardSerializer(dashboard, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        # Soft delete the dashboard entry
        dashboard.is_deleted = True
        dashboard.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


# --------- (SPECIFIC) DASHBOARD VIEWS --------- #


# --- VIEW FOR NET SALES --- #
@api_view(['GET'])
def dashboard_net_sales(request):
    # Calculate net sales within a specified time frame.
    try:
        time_frame = request.query_params.get('time_frame', '24h')
        start_date, _ = get_time_frame_range(time_frame)
        sales_query = query_inventory_history(TRANSACTION_TYPES['sale'], start_date)
        net_sales = calculate_aggregates(
            sales_query.annotate(total_price=F('quantity') * F('inventory__price')),
            {'net_sales': Sum('total_price')}
        )['net_sales'] or 0
        return Response({"net_sales": net_sales, "time_frame": time_frame})
    except ValueError as e:
        return Response({"error": str(e)}, status=400)
    

# --- VIEW FOR TOTAL ORDERS --- #

@api_view(['GET'])
def dashboard_total_orders(request):
    # Calculate total orders within a specified time frame.
    try:
        time_frame = request.query_params.get('time_frame', '24h')
        start_date, _ = get_time_frame_range(time_frame)
        orders_query = query_inventory_history(TRANSACTION_TYPES['sale'], start_date)
        total_orders = orders_query.count()
        return Response({"total_orders": total_orders, "time_frame": time_frame})
    except ValueError as e:
        return Response({"error": str(e)}, status=400)


# --- VIEWS FOR NET PURCHASES - BY CATEGORY --- #

@api_view(['GET'])
def dashboard_net_purchases_by_category(request):
    # Aggregate net purchases by category.
    try:
        time_frame = request.query_params.get('time_frame', '24h')
        start_date, _ = get_time_frame_range(time_frame)
        purchase_query = PurchaseOrder.objects.filter(po_date__gte=start_date) if start_date else PurchaseOrder.objects.all()
        net_purchases = purchase_query.values('inventory__category__name').annotate(
            net_purchase=Sum(F('order_quantity') * F('inventory__cost')),
            total_quantity=Sum('order_quantity')
        ).order_by('inventory__category__name')
        return Response({"net_purchases_by_category": net_purchases, "time_frame": time_frame})
    except ValueError as e:
        return Response({"error": str(e)}, status=400)
    

# --- VIEWS FOR NET PURCHASES - BY ITEM --- #

@api_view(['GET'])
def dashboard_net_purchases_by_item(request):
    # Aggregate net purchases by item.
    try:
        time_frame = request.query_params.get('time_frame', '24h')
        start_date, _ = get_time_frame_range(time_frame)
        purchase_query = query_inventory_history(TRANSACTION_TYPES['restock'], start_date)
        net_purchases = purchase_query.values('inventory__name').annotate(
            net_purchase=Sum(F('quantity') * F('inventory__cost')),
            total_quantity=Sum('quantity')
        ).order_by('inventory__name')
        return Response({"net_purchases_by_item": net_purchases, "time_frame": time_frame})
    except ValueError as e:
        return Response({"error": str(e)}, status=400)


# --- VIEWS FOR BREAKDOWN --- #

@api_view(['GET'])
def dashboard_total_breakdown(request):
    # Provide a detailed breakdown of sales, purchases, shipments, and inventory.
    try:
        # Parse time frame and custom date range
        time_frame = request.query_params.get('time_frame', '24h')
        custom_start = request.query_params.get('start_date')
        custom_end = request.query_params.get('end_date')
        start_date, end_date = get_time_frame_range(time_frame, custom_start, custom_end)

        # Query sales and purchases
        sales_query = query_inventory_history(TRANSACTION_TYPES['sale'], start_date, end_date)
        purchases_query = query_inventory_history(TRANSACTION_TYPES['restock'], start_date, end_date)

        # Calculate totals
        total_sales = calculate_aggregates(sales_query, {'total_sales': Sum('quantity')})['total_sales'] or 0
        total_purchases = calculate_aggregates(purchases_query, {'total_purchases': Sum('quantity')})['total_purchases'] or 0

        # Query shipments
        shipment_query = SalesOrderShipment.objects.exclude(
            tracking_number='0000', shipping_company='To Be Determined'
        )
        shipments_needing_attention_query = SalesOrderShipment.objects.filter(
            Q(tracking_number='0000') | Q(shipping_company='To Be Determined')
        )
        if start_date:
            shipment_query = shipment_query.filter(shipped_date__gte=start_date)
            shipments_needing_attention_query = shipments_needing_attention_query.filter(shipped_date__gte=start_date)
        if end_date:
            shipment_query = shipment_query.filter(shipped_date__lte=end_date)
            shipments_needing_attention_query = shipments_needing_attention_query.filter(shipped_date__lte=end_date)

        total_shipments = shipment_query.count()
        shipments_needing_attention = shipments_needing_attention_query.count()

        # Query inventory breakdown
        breakdown_type = request.query_params.get('breakdown_type', 'item')
        if breakdown_type == 'category':
            inventory_levels = Inventory.objects.values('category__name').annotate(
                total_quantity=Sum('quantity'),
                total_value=Sum(F('quantity') * F('cost'))
            ).order_by('category__name')
        else:  # Default to item-level breakdown
            inventory_levels = Inventory.objects.values('name').annotate(
                total_quantity=Sum('quantity'),
                total_value=Sum(F('quantity') * F('cost'))
            ).order_by('name')

        return Response({
            "total_sales": total_sales,
            "total_purchases": total_purchases,
            "total_shipments": total_shipments,
            "shipments_needing_attention": shipments_needing_attention,
            "current_inventory_levels": inventory_levels,
            "time_frame": time_frame,
            "breakdown_type": breakdown_type,
        })
    except ValueError as e:
        return Response({"error": str(e)}, status=400)
    

# --------- HELPER VIEW FOR VALIDATION --------- #

@api_view(['GET'])
def validate_time_frame(request):
    """Validate and retrieve a time frame from query parameters."""
    time_frame = request.query_params.get('time_frame', '24h')
    try:
        start_date, end_date = get_time_frame_range(time_frame)
        return Response({"start_date": start_date, "end_date": end_date})
    except ValueError as e:
        return Response({"error": str(e)}, status=400)