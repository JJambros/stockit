from datetime import datetime, timedelta        # Added for forecasting
from django.db.models import Avg, Sum                # Added for forecasting
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.authtoken.models import Token 
from django.contrib.auth import authenticate
from django.contrib.auth.models import User  # Built-in User model for auth
from .models import Profile, Inventory, Dashboard, InventoryHistory, AuditTrail, OrderItem, CustomerOrder
from .serializers import ProfileSerializer, InventorySerializer, DashboardSerializer, AuditTrailSerializer, OrderItemSerializer
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

# --------- TRACKING SHIPPING VIEWS --------- #

def mark_order_as_shipped(request, order_id):
    try:
        order = CustomerOrder.objects.get(id=order_id)
    except CustomerOrder.DoesNotExist:
        return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)

    order.shipped = True
    order.save()
    return Response({'message': 'Order marked as shipped successfully'}, status=status.HTTP_200_OK)