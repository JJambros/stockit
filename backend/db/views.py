from datetime import datetime, timedelta        # Added for forecasting
from django.db.models import Avg, Sum                # Added for forecasting
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status 
from django.contrib.auth.models import User  # Built-in User model for auth
from .models import Profile, Inventory, Dashboard, InventoryHistory
from .serializers import ProfileSerializer, InventorySerializer, DashboardSerializer

# Example of data view used for testing
@api_view(['GET'])
def my_data(request):
    data = {
        'message': 'Hello from the db app!'
    }
    return Response(data)


# --------- PROFILE VIEWS (For managing user profiles) --------- #

# Get/update the logged-in user's profile
@api_view(['GET', 'PUT'])
def profile_detail(request):
    user = request.user  # Get the currently logged-in user
    try:
        profile = Profile.objects.get(user=user)
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
        inventory = Inventory.objects.all()
        serializer = InventorySerializer(inventory, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        # Create a new inventory item
        serializer = InventorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Retrieve, update, or delete a specific inventory item
@api_view(['GET', 'PUT', 'DELETE'])
def inventory_detail(request, pk):
    try:
        inventory = Inventory.objects.get(pk=pk)
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
        # Delete the inventory item
        inventory.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# --------- DASHBOARD VIEWS --------- #

# List dashboard data or add a new dashboard item
@api_view(['GET', 'POST'])
def dashboard_list(request):
    if request.method == 'GET':
        # Retrieve all dashboard data
        dashboards = Dashboard.objects.all()
        serializer = DashboardSerializer(dashboards, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        # Add a new dashboard entry
        serializer = DashboardSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Retrieve, update, or delete a specific dashboard entry
@api_view(['GET', 'PUT', 'DELETE'])
def dashboard_detail(request, pk):
    try:
        dashboard = Dashboard.objects.get(pk=pk)
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
        # Delete the dashboard entry
        dashboard.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
# --------- INVENTORY FORECAST VIEWS --------- #

def inventory_forecast(request, inventory_id, forecast_date):
    try:
        inventory = Inventory.objects.get(id=inventory_id)
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
    forecasted_profit = (inventory.price - inventory.cost) * forecasted_sales
    forecasted_expenses = forecasted_sales * inventory.cost

    # Calculate the estimated number of orders based on historical order data
    avg_daily_orders = sales_history.count() / 90  # Orders per day, based on the last 3 months
    forecasted_orders = avg_daily_orders * days_into_future

    # Check if inventory falls below zero and calculate the restocking need
    restock_message = None
    if forecasted_remaining_quantity < 0:
        restock_amount = abs(forecasted_remaining_quantity)  # How much to restock
        restock_message = f"Insufficient quantity. You will need to restock at least {restock_amount} units."

    # Return the forecast results
    return Response({
        'forecast_date': forecast_date,
        'forecasted_profit': forecasted_profit,
        'forecasted_expenses': forecasted_expenses,
        'forecasted_quantity_used': forecasted_sales,
        'forecasted_remaining_quantity': forecasted_remaining_quantity,
        'forecasted_orders': forecasted_orders,
        'restock_message': restock_message
    })