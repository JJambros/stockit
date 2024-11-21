from rest_framework import serializers 
from .models import (UserProfile, Inventory, Customer, Dashboard, ShippingAddress, InventoryHistory, 
                     ForecastingPreferences, ForecastResults, DashboardReports, DashboardVisuals, 
                     ReportDateRange, UserDashSettings, OrderStatus, ReorderThreshold, Supplier,
                     PurchaseOrder, Notifications, SalesOrder, SalesOrderItem, SalesOrderShipment, AuditTrail,
                     WorksOn, InventoryCategory)

# Profile Serializer
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'  # Optionally include 'is_deleted' if needed
        extra_kwargs = {'is_deleted': {'read_only': True}}  # Make 'is_deleted' read-only

# Category Serializer   --> changed to InventoryCategorySerializer
class InventoryCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryCategory
        fields = '__all__'  # or limit to necessary fields
        extra_kwargs = {'is_deleted': {'read_only': True}}  # Make 'is_deleted' read-only

class InventorySerializer(serializers.ModelSerializer):
    item_category = serializers.CharField(source='item_category.inventory_category_name', default='Uncategorized')

    def validate_item_category(self, value):
        # Convert category name to InventoryCategory instance
        category, _ = InventoryCategory.objects.get_or_create(inventory_category_name=value)
        return category

    def create(self, validated_data):
        category_name = validated_data.pop('item_category', {}).get('inventory_category_name', 'Uncategorized')
        validated_data['item_category'], _ = InventoryCategory.objects.get_or_create(inventory_category_name=category_name)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        category_name = validated_data.pop('item_category', {}).get('inventory_category_name', 'Uncategorized')
        instance.item_category, _ = InventoryCategory.objects.get_or_create(inventory_category_name=category_name)
        return super().update(instance, validated_data)

    class Meta:
        model = Inventory
        fields = '__all__'

# Customer Serializer
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'
        extra_kwargs = {'is_deleted': {'read_only': True}}

# Dashboard Serializer
class DashboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dashboard
        fields = '__all__'
        extra_kwargs = {'is_deleted': {'read_only': True}}

# Location Serializer   --> changed to ShippingAddressSerializer
class ShippingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddress
        fields = '__all__'
        extra_kwargs = {'is_deleted': {'read_only': True}}

# InventoryHistory Serializer
class InventoryHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryHistory
        fields = '__all__'
        extra_kwargs = {'is_deleted': {'read_only': True}}

# ForecastingPreferences Serializer
class ForecastingPreferencesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ForecastingPreferences
        fields = '__all__'
        extra_kwargs = {'is_deleted': {'read_only': True}}

# ForecastResults Serializer
class ForecastResultsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ForecastResults
        fields = '__all__'
        extra_kwargs = {'is_deleted': {'read_only': True}}

# DashboardReports Serializer
class DashboardReportsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DashboardReports
        fields = '__all__'
        extra_kwargs = {'is_deleted': {'read_only': True}}

# DashboardVisuals Serializer
class DashboardVisualsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DashboardVisuals
        fields = '__all__'
        extra_kwargs = {'is_deleted': {'read_only': True}}

# ReportDateRange Serializer
class ReportDateRangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportDateRange
        fields = '__all__'
        extra_kwargs = {'is_deleted': {'read_only': True}}

# UserDashboardSettings Serializer
class UserDashSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDashSettings
        fields = '__all__'
        extra_kwargs = {'is_deleted': {'read_only': True}}

# OrderStatus Serializer
class OrderStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderStatus
        fields = '__all__'
        extra_kwargs = {'is_deleted': {'read_only': True}}

# ReorderThreshold Serializer
class ReorderThresholdSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReorderThreshold
        fields = '__all__'
        extra_kwargs = {'is_deleted': {'read_only': True}}

# Supplier Serializer
class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'
        extra_kwargs = {'is_deleted': {'read_only': True}}

# PurchaseOrder Serializer
class PurchaseOrderSerializer(serializers.ModelSerializer):
    # Char.Field supplier_name and inventory_name so that the name appears instead of the db ID number
    supplier_name = serializers.CharField(source='supplier.supplier_name', read_only=True) 
    inventory_name = serializers.CharField(source='inventory.name', read_only=True)

    class Meta:
        model = PurchaseOrder
        fields = '__all__'
        extra_kwargs = {'is_deleted': {'read_only': True}}

# Notifications Serializer
class NotificationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notifications
        fields = '__all__'
        extra_kwargs = {'is_deleted': {'read_only': True}}

# Order Item Serializer --> changed to SalesOrderItemSerializer
class SalesOrderItemSerializer(serializers.ModelSerializer):
    inventory_name = serializers.CharField(source='inventory.name', read_only=True)
    order_name = serializers.CharField(source='order.to_company', read_only=True)

    class Meta:
        model = SalesOrderItem
        fields = ['order_item_id', 'inventory', 'inventory_name', 'order', 'order_name', 'quantity', 'is_deleted']
        extra_kwargs = {
            'is_deleted': {'read_only': True},
            'inventory': {'write_only': True},  # Make 'inventory' and 'order' writable
            'order': {'write_only': True}
        }

# Customer Order Serializer --> changed to SalesOrderSerializer
class SalesOrderSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='status.current_status', read_only=True)
    location_name = serializers.CharField(source='location.address', read_only=True)
    customer_name = serializers.CharField(source='customer.name', read_only=True)
    user_name = serializers.CharField(source='user.username', read_only=True)
    items = SalesOrderItemSerializer(source='orderitem_set', many=True, read_only=True)

    class Meta:
        model = SalesOrder
        fields = '__all__'  # Keeps all model fields and adds the custom readable fields
        extra_kwargs = {'is_deleted': {'read_only': True}, 'shipped': {'read_only': False}}

# Shipment Serializer   --> changed to SalesOrderShipmentSerializer
class SalesOrderShipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesOrderShipment
        fields = '__all__'
        extra_kwargs = {'is_deleted': {'read_only': True}}

class AuditTrailSerializer(serializers.ModelSerializer):
    employee_name = serializers.SerializerMethodField()
    formatted_date = serializers.SerializerMethodField()
    formatted_time = serializers.SerializerMethodField()

    def get_employee_name(self, obj):
        # Access the Profile related to the changed_by user
        return f"{obj.changed_by.first_name} {obj.changed_by.last_name}"

    def get_formatted_date(self, obj):
        # Format the date part of change_time
        return obj.change_time.strftime("%Y-%m-%d")

    def get_formatted_time(self, obj):
        # Format the time part of change_time
        return obj.change_time.strftime("%H:%M:%S")

    class Meta:
        model = AuditTrail
        fields = ['employee_name', 'formatted_date', 'formatted_time', 'changed_desc', 'content_type', 'object_id', 'is_deleted']

# WorksOn Serializer
class WorksOnSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorksOn
        fields = '__all__'
        extra_kwargs = {'is_deleted': {'read_only': True}}
