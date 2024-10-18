from rest_framework import serializers 
from .models import(Profile, Inventory, Customer, Dashboard, Location, InventoryHistory, 
                    ForecastingPreferences, ForecastResults, DashboardReports, DashboardVisuals, 
                    ReportDateRange, UserDashSettings, OrderStatus, ReorderThreshold, Supplier,
                    PurchaseOrder, Notifications, CustomerOrder, OrderItem, Shipment, AuditTrail,
                    WorksOn)

# Profile Serializer
class ProfileSerializer(serializers.ModelSerializer): # ModelSerializer automatically generates set of fields and generate validators for serializer
    class Meta:
        model = Profile
        fields = '__all__' # Indicates that all fields of each model should be used, if this needs to be changed in the future it can be done so by manaully putting in the fields.

# Inventory Serializer
class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = '__all__'

# Customer Serializer
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

# Dashboard Serializer
class DashboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dashboard
        fields = '__all__'

# Location Serializer
class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'

# InventoryHistory Serializer
class InventoryHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryHistory
        fields = '__all__'

# ForecastingPreferences Serializer
class ForecastingPreferencesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ForecastingPreferences
        fields = '__all__'

# ForecastResults Serializer
class ForecastResultsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ForecastResults
        fields = '__all__'

# DashboardReports Serializer
class DashboardReportsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DashboardReports
        fields = '__all__'

# DashboardVisuals Serializer
class DashboardVisualsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DashboardVisuals
        fields = '__all__'

# ReportDateRange Serializer
class ReportDateRangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportDateRange
        fields = '__all__'

# UserDashboardSettings Serializer
class UserDashSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDashSettings
        fields = '__all__'

# OrderStatus Serializer
class OrderStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderStatus
        fields = '__all__'

# ReorderThreshold Serializer
class ReorderThresholdSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReorderThreshold
        fields = '__all__'

# Supplier Serializer
class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'

# PurchaseOrder Serializer
class PurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = '__all__'

# Notifications Serializer
class NotificationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notifications
        fields = '__all__'

# CustomerOrder Serializer
class CustomerOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerOrder
        fields = '__all__'

# Order Item Serializer
class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'

# Shipment Serializer
class ShipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipment
        fields = '__all__'

# AuditTrail Serializer
class AuditTrailSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditTrail
        fields = '__all__'

# WorksOn Serializer
class WorksOnSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorksOn
        fields = '__all__'