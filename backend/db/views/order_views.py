from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from ..models import SalesOrderItem, SalesOrder, ShippingAddress, OrderStatus
from ..serializers import SalesOrderItemSerializer, SalesOrderSerializer, ShippingAddressSerializer, OrderStatusSerializer


# --------- SALES ORDER ITEM VIEWS --------- # 

@api_view(['GET', 'POST'])
def sales_order_item_list(request):
    if request.method == 'GET':
        order_items = SalesOrderItem.objects.filter(is_deleted=False)
        serializer = SalesOrderItemSerializer(order_items, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = SalesOrderItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# --------- SALES ORDER VIEWS (formally 'Customer Order')--------- #

@api_view(['GET', 'POST'])
def sales_order_list(request):
    if request.method == 'GET':
        orders = SalesOrder.objects.filter(is_deleted=False)
        serializer = SalesOrderSerializer(orders, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = SalesOrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def sales_order_detail(request, pk):
    try:
        order = SalesOrder.objects.get(pk=pk, is_deleted=False)
    except SalesOrder.DoesNotExist:
        return Response({'error': 'Customer Order not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SalesOrderSerializer(order)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = SalesOrderSerializer(order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        order.is_deleted = True
        order.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


# --------- ORDER STATUS VIEWS --------- # 

@api_view(['GET', 'POST'])
def order_status_list(request):
    if request.method == 'GET':
        order_statuses = OrderStatus.objects.all()
        serializer = OrderStatusSerializer(order_statuses, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = OrderStatusSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def order_status_detail(request, pk):
    try:
        order_status = OrderStatus.objects.get(pk=pk)
    except OrderStatus.DoesNotExist:
        return Response({'error': 'Order status not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = OrderStatusSerializer(order_status)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = OrderStatusSerializer(order_status, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        order_status.delete()
        return Response({'message': 'Order status deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

# --------- INDEX VIEWS --------- #

@api_view(['GET'])
def index_view(request):
    return Response({"message": "Welcome to the API index"})
