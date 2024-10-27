from rest_framework import serializers 
from .models import (Profile, Inventory, Customer, Dashboard, Location, InventoryHistory, 
                     ForecastingPreferences, ForecastResults, DashboardReports, DashboardVisuals, 
                     ReportDateRange, UserDashSettings, OrderStatus, ReorderThreshold, Supplier,
                     PurchaseOrder, Notifications, CustomerOrder, OrderItem, Shipment, AuditTrail,
                     WorksOn)

# Profile Serializer
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'  # Optionally include 'is_deleted' if needed
        extra_kwargs = {'is_deleted': {'read_only': True}}  # Make 'is_deleted' read-only

# Inventory Serializer
class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = '__all__'
        extra_kwargs = {'is_deleted': {'read_only': True}}

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

# CustomerOrder Serializer
class CustomerOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerOrder
        fields = '__all__'
        extra_kwargs = {'is_deleted': {'read_only': True}, 'shipped': {'read_only': False}}

# Order Item Serializer
class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'
        extra_kwargs = {'is_deleted': {'read_only': True}}

# Shipment Serializer
class ShipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipment
        fields = '__all__'
        extra_kwargs = {'is_deleted': {'read_only': True}}

# AuditTrail Serializer (If AuditTrail should not support soft deletion, omit 'is_deleted')
class AuditTrailSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditTrail
        fields = '__all__'

# WorksOn Serializer
class WorksOnSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorksOn
        fields = '__all__'
        extra_kwargs = {'is_deleted': {'read_only': True}}
