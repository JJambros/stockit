from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.shortcuts import render 
from ..models import Inventory, InventoryCategory, InventoryHistory
from ..serializers import InventorySerializer, InventoryCategorySerializer, InventoryHistorySerializer


# --------- INVENTORY VIEWS --------- #

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


@api_view(['GET', 'PUT', 'DELETE'])
def inventory_detail(request, pk):
    try:
        inventory = Inventory.objects.get(pk=pk, is_deleted=False)  # Ensure the item is not soft-deleted
    except Inventory.DoesNotExist:
        return Response({'error': 'Inventory item not found.'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        # Retrieve a single inventory item
        serializer = InventorySerializer(inventory)
        return Response(serializer.data)

    elif request.method == 'PUT':
        # Update an inventory item
        serializer = InventorySerializer(inventory, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        # Soft-delete an inventory item
        inventory.is_deleted = True
        inventory.save()
        return Response({'message': 'Inventory item soft-deleted.'}, status=status.HTTP_204_NO_CONTENT)



# --------- INVENTORY CATEGORY VIEWS --------- #

# List all categories or create a new one
@api_view(['GET', 'POST'])
def inventory_category_list(request):
    if request.method == 'GET':
        # Retrieve all categories excluding soft-deleted ones
        categories = InventoryCategory.objects.filter(is_deleted=False)
        serializer = InventoryCategorySerializer(categories, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        # Create a new category
        serializer = InventoryCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Retrieve, update, or delete a specific category
@api_view(['GET', 'PUT', 'DELETE'])
def inventory_category_detail(request, pk):
    try:
        category = InventoryCategory.objects.get(pk=pk, is_deleted=False)
    except InventoryCategory.DoesNotExist:
        return Response({'error': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = InventoryCategorySerializer(category)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = InventoryCategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        # Soft delete the category
        category.is_deleted = True
        category.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


# --------- INVENTORY HISTORY VIEW --------- # 

@api_view(['GET', 'POST'])
def inventory_history_view(request):
    history_items = InventoryHistory.objects.all().order_by('-transaction_date')
    return render(request, 'inventory_history.html', {'history_items': history_items})


# --------- INVENTORY UPDATE --------- # 

@api_view(['PUT'])
def update_inventory(request, pk):
    try:
        inventory_item = Inventory.objects.get(pk=pk)
    except Inventory.DoesNotExist:
        return Response({'error': 'Inventory item not found'}, status=status.HTTP_404_NOT_FOUND)

    data = request.data
    category_name = data.get('item_category', None)

    if category_name:
        category, _ = InventoryCategory.objects.get_or_create(
            inventory_category_name=category_name
        )
        inventory_item.item_category = category

    inventory_item.item_name = data.get('item_name', inventory_item.item_name)
    inventory_item.item_cost = data.get('item_cost', inventory_item.item_cost)
    inventory_item.item_price = data.get('item_price', inventory_item.item_price)
    inventory_item.item_quantity = data.get('item_quantity', inventory_item.item_quantity)
    inventory_item.save()
    return Response({'message': 'Inventory updated successfully'}, status=status.HTTP_200_OK)

