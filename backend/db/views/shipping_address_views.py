from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from ..models import ShippingAddress
from ..serializers import ShippingAddressSerializer


# --------- SHIPPING ADDRESS VIEWS --------- #

@api_view(['GET', 'POST'])
def shipping_address_list(request):
    if request.method == 'GET':
        locations = ShippingAddress.objects.all()
        serializer = ShippingAddressSerializer(locations, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ShippingAddressSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def shipping_address_detail(request, pk):
    try:
        location = ShippingAddress.objects.get(pk=pk)
    except ShippingAddress.DoesNotExist:
        return Response({'error': 'Location not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ShippingAddressSerializer(location)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = ShippingAddressSerializer(location, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        location.delete()
        return Response({'message': 'Location deleted successfully'}, status=status.HTTP_204_NO_CONTENT)