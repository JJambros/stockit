from django.db.models import Q  # Added for forecasting and dashboard (net calcs & breakdown)
from rest_framework.response import Response
from rest_framework.decorators import api_view
from ..models import UserProfile, Inventory, SalesOrder
from ..serializers import UserProfileSerializer, InventorySerializer, SalesOrderSerializer


# --------- SEARCH BAR VIEWS --------- #

@api_view(['GET'])
def search_view(request):
    query = request.query_params.get('q', '')

    # Retrieve sorting and filtering parameters
    sort_by = request.query_params.get('sort_by', '')  # e.g., 'category', 'quantity', 'name', 'date', 'shipping_status'
    order = request.query_params.get('order', 'asc')  # e.g., 'asc' for ascending, 'desc' for descending
    start_date = request.query_params.get('start_date', '')  # For date filtering
    end_date = request.query_params.get('end_date', '')

    # Initialize result lists
    profile_results = []
    inventory_results = []
    order_results = []

    if query:
        # Profiles Search
        profiles = UserProfile.objects.filter(
            Q(Fname__icontains=query) | Q(Lname__icontains=query) | Q(email__icontains=query),
            is_deleted=False
        )
        profile_results = UserProfileSerializer(profiles, many=True).data

        # Inventory Search with Sorting and Filtering
        inventory_items = Inventory.objects.filter(
            Q(name__icontains=query) | Q(category__name__icontains=query),
            is_deleted=False
        )
        
        # Apply sorting for Inventory
        if sort_by == 'category':
            inventory_items = inventory_items.order_by('category__name' if order == 'asc' else '-category__name')
        elif sort_by == 'quantity':
            inventory_items = inventory_items.order_by('quantity' if order == 'asc' else '-quantity')
        elif sort_by == 'name':
            inventory_items = inventory_items.order_by('name' if order == 'asc' else '-name')
        
        inventory_results = InventorySerializer(inventory_items, many=True).data

        # Customer Order Search with Sorting and Date Filtering
        orders = SalesOrder.objects.filter(
            Q(from_company__icontains=query) | Q(to_company__icontains=query),
            is_deleted=False
        )

        # Apply date filtering for orders
        if start_date and end_date:
            orders = orders.filter(customer_order_date__range=[start_date, end_date])

        # Apply sorting for Customer Orders
        if sort_by == 'date':
            orders = orders.order_by('customer_order_date' if order == 'asc' else '-customer_order_date')
        elif sort_by == 'shipping_status':
            orders = orders.order_by('status__current_status' if order == 'asc' else '-status__current_status')

        order_results = SalesOrderSerializer(orders, many=True).data

    # Combine results
    results = {
        'profiles': profile_results,
        'inventory': inventory_results,
        'orders': order_results,
    }

    return Response(results)
