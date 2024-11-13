from rest_framework import serializers 
from .models import (Profile, Inventory, Customer, Dashboard, Location, InventoryHistory,
                     ForecastingPreferences, ForecastResults, DashboardReports, DashboardVisuals, 
                     ReportDateRange, UserDashSettings, OrderStatus, ReorderThreshold, Supplier, SupplierOrder,
                     PurchaseOrder, Notifications, CustomerOrder, OrderItem, Shipment, AuditTrail,
                     WorksOn, Category)

# Profile Serializer
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'  # Optionally include 'is_deleted' if needed
        extra_kwargs = {'is_deleted': {'read_only': True}}  # Make 'is_deleted' read-only

# Category Serializer
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'  # or limit to necessary fields
        extra_kwargs = {'is_deleted': {'read_only': True}}  # Make 'is_deleted' read-only

# Inventory Serializer
class InventorySerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    class Meta:
        model = Inventory
        fields = '__all__'
        extra_kwargs = {'is_deleted': {'read_only': True}}  # Make 'is_deleted' read-only

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

# Location Serializer
class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
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

# SupplierOrder Serializer
class SupplierOrderSerializer(serializers.ModelSerializer):
    supplier_name = serializers.CharField(source='supplier.supplier_name', read_only=True)
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = SupplierOrder
        fields = ['supplier_order_id', 'supplier', 'supplier_name', 'product', 'product_name', 'quantity', 'status',
                  'created_at']
        extra_kwargs = {
            'status': {'read_only': False},
            'created_at': {'read_only': True}
        }

# PurchaseOrder Serializer
class PurchaseOrderSerializer(serializers.ModelSerializer):
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

# Order Item Serializer
class OrderItemSerializer(serializers.ModelSerializer):
    inventory_name = serializers.CharField(source='inventory.name', read_only=True)

    class Meta:
        model = OrderItem
        fields = '__all__'
        extra_kwargs = {'is_deleted': {'read_only': True}}

# Customer Order Serializer
class CustomerOrderSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='status.current_status', read_only=True)
    location_name = serializers.CharField(source='location.address', read_only=True)
    customer_name = serializers.CharField(source='customer.name', read_only=True)
    user_name = serializers.CharField(source='user.username', read_only=True)
    items = OrderItemSerializer(source='orderitem_set', many=True, read_only=True)

    class Meta:
        model = CustomerOrder
        fields = '__all__'  # Keeps all model fields and adds the custom readable fields
        extra_kwargs = {'is_deleted': {'read_only': True}, 'shipped': {'read_only': False}}

# Shipment Serializer
class ShipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipment
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
