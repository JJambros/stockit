from datetime import datetime, timedelta  # Added for forecasting and dashboard (net calcs)
from django.db.models import Avg
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from ..models import Inventory, InventoryHistory, ForecastingPreferences
from ..serializers import ForecastingPreferencesSerializer
from decimal import Decimal  # Added because math is dumb (decimals and floats can't multiply)


# --------- INVENTORY FORECAST VIEWS --------- #

@api_view(['GET'])
def inventory_forecast(request, inventory_id, forecast_date):
    try:
        inventory = Inventory.objects.get(inventory_id=inventory_id, is_deleted=False)
    except Inventory.DoesNotExist:
        return Response({'error': 'Inventory not found'}, status=404)

    try:
        forecast_date = datetime.strptime(forecast_date, '%Y-%m-%d').date()
    except ValueError:
        return Response({'error': 'Invalid date format. Use YYYY-MM-DD.'}, status=400)

    # Get query parameters with default values
    trend_direction = request.query_params.get('trend_direction')
    trend_percent = Decimal(request.query_params.get('trend_percent', 0)) / 100
    start_date = request.query_params.get('start_date')
    end_date = request.query_params.get('end_date')

    # Convert dates if provided
    if start_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
    else:
        start_date = datetime.now().date() - timedelta(days=90)  # Default 3 months

    if end_date:
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
    else:
        end_date = datetime.now().date()

    # Fetch historical data within the date range
    sales_history = InventoryHistory.objects.filter(
        inventory=inventory,
        transaction_type='sale',
        transaction_date__range=(start_date, end_date)
    )

    if not sales_history.exists():
        return Response({'error': 'Not enough historical data for forecasting'}, status=400)

    avg_daily_sales = sales_history.aggregate(Avg('quantity'))['quantity__avg']
    days_into_future = (forecast_date - datetime.now().date()).days
    forecasted_sales = Decimal(avg_daily_sales * days_into_future)

    # Apply trend adjustment
    if trend_direction == 'increase':
        forecasted_sales *= (1 + trend_percent)
    elif trend_direction == 'decrease':
        forecasted_sales *= (1 - trend_percent)

    forecasted_remaining_quantity = inventory.quantity - forecasted_sales
    forecasted_profit = (Decimal(inventory.price) - Decimal(inventory.cost)) * forecasted_sales
    forecasted_expenses = Decimal(forecasted_sales) * Decimal(inventory.cost)
    avg_daily_orders = sales_history.count() / 90
    forecasted_orders = avg_daily_orders * days_into_future

    # Update the restock message with rounded value
    if forecasted_remaining_quantity < 0:
        restock_amount = abs(forecasted_remaining_quantity)  # How much to restock
        restock_message = f"Insufficient quantity. You will need to restock at least {round(restock_amount, 2)} units."
    else:
        restock_message = None

    # New responses added
    return Response({
        'forecast_date': forecast_date,
        'trend_direction': trend_direction,
        'trend_percent': float(trend_percent) * 100,  # Convert back for display
        'start_date': start_date,
        'end_date': end_date,
        'forecasted_profit': round(float(forecasted_profit), 2),
        'forecasted_expenses': round(float(forecasted_expenses), 2),
        'forecasted_quantity_used': round(forecasted_sales, 2),
        'forecasted_remaining_quantity': round(forecasted_remaining_quantity, 2),
        'forecasted_orders': round(forecasted_orders, 2),
        'restock_message': restock_message
    })


# --------- FORECASTING ADJUST (due to special conditions) --------- #

@api_view(['POST'])
def adjust_forecast(request):
    serializer = ForecastingPreferencesSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# --------- FORECASTING PREFERENCES VIEWS  --------- #

@api_view(['GET', 'POST'])
def forecasting_preferences_list(request):
    if request.method == 'GET':
        preferences = ForecastingPreferences.objects.filter(is_deleted=False)
        serializer = ForecastingPreferencesSerializer(preferences, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ForecastingPreferencesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def forecasting_preferences_detail(request, pk):
    try:
        preference = ForecastingPreferences.objects.get(pk=pk, is_deleted=False)
    except ForecastingPreferences.DoesNotExist:
        return Response({'error': 'Forecasting Preferences not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ForecastingPreferencesSerializer(preference)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ForecastingPreferencesSerializer(preference, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        preference.is_deleted = True
        preference.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

