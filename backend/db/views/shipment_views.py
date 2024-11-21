from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from ..models import SalesOrder, SalesOrderShipment
from ..serializers import SalesOrderShipmentSerializer


# --------- SHIPMENT VIEWS --------- #

# List all shipments or create a new shipment
@api_view(['GET', 'POST'])
def sales_order_shipment_list(request):
    if request.method == 'GET':
        # Retrieve all shipments, excluding soft-deleted ones
        shipments = SalesOrderShipment.objects.filter(is_deleted=False)
        serializer = SalesOrderShipmentSerializer(shipments, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        # Create a new shipment
        serializer = SalesOrderShipmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Retrieve, update, or soft delete a specific shipment
@api_view(['GET', 'PUT', 'DELETE'])
def sales_order_shipment_detail(request, pk):
    try:
        shipment = SalesOrderShipment.objects.get(pk=pk, is_deleted=False)
    except SalesOrderShipment.DoesNotExist:
        return Response({'error': 'Shipment not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        # Return shipment details
        serializer = SalesOrderShipmentSerializer(shipment)
        return Response(serializer.data)

    elif request.method == 'PUT':
        # Update shipment
        serializer = SalesOrderShipmentSerializer(shipment, data=request.data)
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
        order = SalesOrder.objects.get(order_id=order_id)
    except SalesOrder.DoesNotExist:
        return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)

    order.shipped = True
    order.save()
    return Response({'message': 'Order marked as shipped successfully'}, status=status.HTTP_200_OK)
