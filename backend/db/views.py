from django.utils import timezone               # Added for dashboard (net calcs)
from datetime import datetime, timedelta        # Added for forecasting and dashboard (net calcs)
from django.db.models import Avg, Sum, F, Q, Count        # Added for forecasting and dashboard (net calcs & breakdown)
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.authtoken.models import Token 
from django.contrib.auth import authenticate
from django.contrib.auth.models import User  # Built-in User model for auth
from .models import Profile, Inventory, Dashboard, InventoryHistory, AuditTrail, OrderItem, CustomerOrder, Shipment, PurchaseOrder
from .serializers import ProfileSerializer, InventorySerializer, DashboardSerializer, AuditTrailSerializer, OrderItemSerializer, ShipmentSerializer, PurchaseOrderSerializer
from decimal import Decimal # Added because math is dumb (decimals and floats can't multiply)

# Example of data view used for testing
@api_view(['GET'])
def my_data(request):
    data = {
        'message': 'Hello from the db app!'
    }
    return Response(data)


# --------- AUTHENTICATION VIEWS --------- #

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)

    if user is not None:
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'user_id': user.id}, status=status.HTTP_200_OK)
    return Response({'error': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def logout_view(request):
    request.user.auth_token.delete()
    return Response({'success': 'Logged out'}, status=status.HTTP_200_OK)


# --------- PROFILE VIEWS (For managing user profiles) --------- #

# Get/update the logged-in user's profile
@api_view(['GET', 'PUT'])
def profile_detail(request):
    user = request.user  # Get the currently logged-in user
    try:
        profile = Profile.objects.get(user=user, is_deleted=False) # Check for soft deletion
    except Profile.DoesNotExist:
        return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        # Return the user's profile information
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    elif request.method == 'PUT':
        # Update the user's profile
        serializer = ProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# --------- INVENTORY VIEWS --------- #

# List all inventory items or add a new item
@api_view(['GET', 'POST'])
def inventory_list(request):
    if request.method == 'GET':
        # Retrieve all inventory items
        inventory = Inventory.objects.filter(is_deleted=False)  # Exclude soft-deleted items
        serializer = InventorySerializer(inventory, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        # Create a new inventory item
        serializer = InventorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Retrieve, update, or soft-delete a specific inventory item
@api_view(['GET', 'PUT', 'DELETE'])
def inventory_detail(request, pk):
    try:
        inventory = Inventory.objects.get(pk=pk, is_deleted=False)
    except Inventory.DoesNotExist:
        return Response({'error': 'Inventory not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        # Return inventory item details
        serializer = InventorySerializer(inventory)
        return Response(serializer.data)

    elif request.method == 'PUT':
        # Update inventory item
        serializer = InventorySerializer(inventory, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        # Soft delete the inventory item
        inventory.is_deleted = True
        inventory.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


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


# --------- INVENTORY FORECAST VIEWS --------- #

@api_view(['GET'])
def inventory_forecast(request, inventory_id, forecast_date):
    try:
        inventory = Inventory.objects.get(inventory_id=inventory_id, is_deleted=False)  # Check for soft deletion
    except Inventory.DoesNotExist:
        return Response({'error': 'Inventory not found'}, status=404)

    # Convert the input forecast_date to a date object
    try:
        forecast_date = datetime.strptime(forecast_date, '%Y-%m-%d').date()
    except ValueError:
        return Response({'error': 'Invalid date format. Use YYYY-MM-DD.'}, status=400)

    # Fetch historical sales data (past 3 months)
    three_months_ago = datetime.now().date() - timedelta(days=90)
    sales_history = InventoryHistory.objects.filter(
        inventory=inventory, 
        transaction_type='sale', 
        transaction_date__gte=three_months_ago
    )

    if not sales_history.exists():
        return Response({'error': 'Not enough historical data for forecasting'}, status=400)

    # Calculate the average daily sales
    avg_daily_sales = sales_history.aggregate(Avg('quantity'))['quantity__avg']

    # Calculate the number of days between today and the forecast date
    days_into_future = (forecast_date - datetime.now().date()).days

    # Forecasted sales and quantity used
    forecasted_sales = avg_daily_sales * days_into_future
    forecasted_remaining_quantity = inventory.quantity - forecasted_sales

    # Calculate profit as (price - cost) * forecasted quantity sold
    forecasted_profit = (Decimal(inventory.price) - Decimal(inventory.cost)) * Decimal(forecasted_sales)
    forecasted_expenses = Decimal(forecasted_sales) * Decimal(inventory.cost)

    # Calculate the estimated number of orders based on historical order data
    avg_daily_orders = sales_history.count() / 90  # Orders per day, based on the last 3 months
    forecasted_orders = avg_daily_orders * days_into_future

    # Updated response with rounding to 2 decimal places
    forecasted_profit = round(float(forecasted_profit), 2)
    forecasted_expenses = round(float(forecasted_expenses), 2)
    forecasted_quantity_used = round(forecasted_sales, 2)
    forecasted_remaining_quantity = round(forecasted_remaining_quantity, 2)
    forecasted_orders = round(forecasted_orders, 2)

    # Update the restock message with rounded value
    if forecasted_remaining_quantity < 0:
        restock_amount = abs(forecasted_remaining_quantity)  # How much to restock
        restock_message = f"Insufficient quantity. You will need to restock at least {round(restock_amount, 2)} units."
    else:
        restock_message = None

    # Return the forecast results
    return Response({
        'forecast_date': forecast_date,
        'forecasted_profit': round(float(forecasted_profit), 2),
        'forecasted_expenses': round(float(forecasted_expenses), 2),
        'forecasted_quantity_used': round(forecasted_sales, 2),
        'forecasted_remaining_quantity': round(forecasted_remaining_quantity, 2),
        'forecasted_orders': round(forecasted_orders, 2),
        'restock_message': restock_message
    })


# --------- AUDIT TRAIL VIEWS --------- #

@api_view(['GET'])
@permission_classes([AllowAny])
def audit_trail_list(request):
    audit_trails = AuditTrail.objects.all()  # No need to filter by 'is_deleted' if AuditTrail is permanent
    serializer = AuditTrailSerializer(audit_trails, many=True)
    return Response(serializer.data)


# --------- ORDER ITEM VIEWS --------- #

@api_view(['GET'])
def order_item_list(request):
    order_items = OrderItem.objects.filter(is_deleted=False)  # Exclude soft-deleted items
    serializer = OrderItemSerializer(order_items, many=True)
    return Response(serializer.data)


# --------- INDEX VIEWS --------- #

@api_view(['GET'])
def index_view(request):
    return Response({"message": "Welcome to the API index"})

# --------- SHIPMENT VIEWS --------- # 

# List all shipments or create a new shipment
@api_view(['GET', 'POST'])
def shipment_list(request):
    if request.method == 'GET':
        # Retrieve all shipments, excluding soft-deleted ones
        shipments = Shipment.objects.filter(is_deleted=False)
        serializer = ShipmentSerializer(shipments, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        # Create a new shipment
        serializer = ShipmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Retrieve, update, or soft delete a specific shipment
@api_view(['GET', 'PUT', 'DELETE'])
def shipment_detail(request, pk):
    try:
        shipment = Shipment.objects.get(pk=pk, is_deleted=False)
    except Shipment.DoesNotExist:
        return Response({'error': 'Shipment not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        # Return shipment details
        serializer = ShipmentSerializer(shipment)
        return Response(serializer.data)

    elif request.method == 'PUT':
        # Update shipment
        serializer = ShipmentSerializer(shipment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        # Soft delete the shipment
        shipment.is_deleted = True
        shipment.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


    # --- TRACKING SHIPPING VIEWS --- #
@api_view(['POST'])
def mark_order_as_shipped(request, order_id):
    try:
        order = CustomerOrder.objects.get(order_id=order_id)
    except CustomerOrder.DoesNotExist:
        return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)

    order.shipped = True
    order.save()
    return Response({'message': 'Order marked as shipped successfully'}, status=status.HTTP_200_OK)


# --------- DASHBOARD VIEWS --------- #


    # --- VIEW FOR NET SALES --- #
@api_view(['GET'])
def dashboard_net_sales(request):
    # Get the time frame from request parameters
    time_frame = request.query_params.get('time_frame', '24h')

    # Determine the date range based on the time frame
    if time_frame == '24h':
        start_date = timezone.now() - timedelta(hours=24)
    elif time_frame == 'week':
        start_date = timezone.now() - timedelta(weeks=1)
    elif time_frame == 'month':
        start_date = timezone.now() - timedelta(days=30)
    elif time_frame == 'overall':
        start_date = None  # No filter for 'overall'
    else:
        return Response({"error": "Invalid time frame"}, status=400)

    # Filter InventoryHistory entries based on time frame and transaction type 'sale'
    history_query = InventoryHistory.objects.filter(transaction_type='sale')
    if start_date:
        history_query = history_query.filter(transaction_date__gte=start_date)

    # Calculate net sales by summing quantity * price for the filtered transactions
    net_sales = (
        history_query.annotate(total_price=F('quantity') * F('inventory__price'))
        .aggregate(net_sales=Sum('total_price'))['net_sales'] or 0
    )

    return Response({"net_sales": net_sales, "time_frame": time_frame})


    # --- VIEW FOR TOTAL ORDERS --- #

@api_view(['GET'])
def dashboard_total_orders(request):
    # Get the time frame from request parameters
    time_frame = request.query_params.get('time_frame')

    # Determine the date range based on the time frame
    if time_frame == '24h':
        start_date = timezone.now() - timedelta(hours=24)
    elif time_frame == 'week':
        start_date = timezone.now() - timedelta(weeks=1)
    elif time_frame == 'month':
        start_date = timezone.now() - timedelta(days=30)
    elif time_frame == 'overall':
        start_date = None  # No filter for 'overall'
    else:
        return Response({"error": "Invalid time frame"}, status=400)

    # Filter InventoryHistory entries for 'sale' transactions and within the specified time frame
    orders_query = InventoryHistory.objects.filter(transaction_type='sale')
    if start_date:
        orders_query = orders_query.filter(transaction_date__gte=start_date)

    # Count the total orders (each sale transaction is considered an order)
    total_orders = orders_query.count()

    return Response({"total_orders": total_orders, "time_frame": time_frame})


    # --- VIEWS FOR NET PURCHASES - BY CATEGORY --- #

@api_view(['GET'])
def dashboard_net_purchases_by_category(request):
    # Get the time frame from request parameters
    time_frame = request.query_params.get('time_frame', '24h')

    # Determine the date range based on the time frame
    if time_frame == '24h':
        start_date = timezone.now() - timedelta(hours=24)
    elif time_frame == 'week':
        start_date = timezone.now() - timedelta(weeks=1)
    elif time_frame == 'month':
        start_date = timezone.now() - timedelta(days=30)
    elif time_frame == 'overall':
        start_date = None  # No filter for 'overall'
    else:
        return Response({"error": "Invalid time frame"}, status=400)

    # Filter PurchaseOrder by date range
    purchase_query = PurchaseOrder.objects.all()
    if start_date:
        purchase_query = purchase_query.filter(po_date__gte=start_date)

    # Aggregate net purchases and total quantity by category
    net_purchases_by_category = (
        purchase_query.values('inventory__category__name')  # Group by category name
        .annotate(
            net_purchase=Sum(F('order_quantity') * F('inventory__cost')),
            total_quantity=Sum('order_quantity')
        )
        .order_by('inventory__category__name')
    )

    return Response({
        "net_purchases_by_category": net_purchases_by_category,
        "time_frame": time_frame
    })


    # --- VIEWS FOR NET PURCHASES - BY ITEM --- #

@api_view(['GET'])
def dashboard_net_purchases_by_item(request):
    # Get the time frame from request parameters
    time_frame = request.query_params.get('time_frame', '24h')

    # Determine the date range based on the time frame
    if time_frame == '24h':
        start_date = timezone.now() - timedelta(hours=24)
    elif time_frame == 'week':
        start_date = timezone.now() - timedelta(weeks=1)
    elif time_frame == 'month':
        start_date = timezone.now() - timedelta(days=30)
    elif time_frame == 'overall':
        start_date = None  # No filter for 'overall'
    else:
        return Response({"error": "Invalid time frame"}, status=400)

    # Filter InventoryHistory for restock transactions within the time frame
    history_query = InventoryHistory.objects.filter(transaction_type='restock')
    if start_date:
        history_query = history_query.filter(transaction_date__gte=start_date)

    # Aggregate net purchases and total quantity by item
    net_purchases_by_item = (
        history_query.values('inventory__name')  # Group by inventory item name
        .annotate(
            net_purchase=Sum(F('quantity') * F('inventory__cost')),
            total_quantity=Sum('quantity')
        )
        .order_by('inventory__name')
    )

    return Response({
        "net_purchases_by_item": net_purchases_by_item,
        "time_frame": time_frame
    })

    
    # --- VIEWS FOR BREAKDOWN --- #

@api_view(['GET'])
def dashboard_total_breakdown(request):
    # Get time frame from request parameters
    time_frame = request.query_params.get('time_frame', '24h')
    start_date = None  # Default to no filter if 'overall'

    # Custom date frame inputs
    custom_start = request.query_params.get('start_date')
    custom_end = request.query_params.get('end_date')

    # Calculate date range based on time frame
    if custom_start and custom_end:
        start_date = timezone.datetime.strptime(custom_start, '%Y-%m-%d').date()
        end_date = timezone.datetime.strptime(custom_end, '%Y-%m-%d').date()
    elif time_frame == '24h':
        start_date = timezone.now() - timedelta(hours=24)
    elif time_frame == 'week':
        start_date = timezone.now() - timedelta(weeks=1)
    elif time_frame == 'month':
        start_date = timezone.now() - timedelta(days=30)
    elif time_frame == 'overall':
        start_date = None

    # Filter InventoryHistory entries for sales and purchases
    sales_query = InventoryHistory.objects.filter(transaction_type='sale')
    purchases_query = InventoryHistory.objects.filter(transaction_type='restock')
    if start_date:
        sales_query = sales_query.filter(transaction_date__gte=start_date)
        purchases_query = purchases_query.filter(transaction_date__gte=start_date)
        if 'end_date' in locals():
            sales_query = sales_query.filter(transaction_date__lte=end_date)
            purchases_query = purchases_query.filter(transaction_date__lte=end_date)

    # Sales and Purchases Counts
    total_sales = sales_query.aggregate(total_sales=Sum('quantity'))['total_sales'] or 0
    total_purchases = purchases_query.aggregate(total_purchases=Sum('quantity'))['total_purchases'] or 0

    # Filter Shipments for assigned shipments and shipments in need of attention
    shipment_query = Shipment.objects.exclude(tracking_number='0000', shipping_company='To Be Determined')
    shipments_needing_attention_query = Shipment.objects.filter(Q(tracking_number='0000') | Q(shipping_company='To Be Determined'))

    if start_date:
        shipment_query = shipment_query.filter(shipped_date__gte=start_date)
        shipments_needing_attention_query = shipments_needing_attention_query.filter(shipped_date__gte=start_date)
        if 'end_date' in locals():
            shipment_query = shipment_query.filter(shipped_date__lte=end_date)
            shipments_needing_attention_query = shipments_needing_attention_query.filter(shipped_date__lte=end_date)

    total_shipments = shipment_query.count()
    shipments_needing_attention = shipments_needing_attention_query.count()

    # Current Inventory Levels (quantity and cost per item or category)
    breakdown_type = request.query_params.get('breakdown_type', 'item')  # 'item' or 'category'

    # Should allow the user to view either by category or by item, instead of having to do this separately
    if breakdown_type == 'category':
        current_inventory_levels = (
            Inventory.objects.values('category__name')
            .annotate(
                total_quantity=Sum('quantity'),
                total_value=Sum(F('quantity') * F('cost'))
            )
            .order_by('category__name')
        )
    else:  # Default to breakdown by item
        current_inventory_levels = (
            Inventory.objects.values('name')
            .annotate(
                total_quantity=Sum('quantity'),
                total_value=Sum(F('quantity') * F('cost'))
            )
            .order_by('name')
        )

    return Response({
        "total_sales": total_sales,
        "total_purchases": total_purchases,
        "total_shipments": total_shipments,
        "shipments_needing_attention": shipments_needing_attention,
        "current_inventory_levels": current_inventory_levels,
        "time_frame": time_frame,
        "breakdown_type": breakdown_type,
    })