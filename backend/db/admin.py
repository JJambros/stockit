from django.contrib import admin
from .models import Profile, Inventory, Customer, Dashboard, Location, InventoryHistory, \
    ForecastingPreferences, ForecastResults, DashboardReports, DashboardVisuals, ReportDateRange, \
    UserDashSettings, OrderStatus, ReorderThreshold, Supplier, PurchaseOrder, Notifications, \
    CustomerOrder, OrderItem, Shipment, AuditTrail, WorksOn  # Import your model


# Ensurees everytime a customer order is saved an audit trail is created
class CustomerOrderAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.save()
        # Pass user to the signal when saving the model
        create_audit_trail_on_save(sender=CustomerOrder, instance=obj, created=not change, user=request.user)


# Ensures that AuditTrail entries are deleted before the CustomerOrder is deleted
class CustomerOrderAdmin(admin.ModelAdmin):
    def delete_model(self, request, obj):
        # Delete related AuditTrail entries first
        AuditTrail.objects.filter(order=obj).delete()
        obj.delete()


# Register your models here.
admin.site.register(Profile)
admin.site.register(Inventory)
admin.site.register(Customer)
admin.site.register(Dashboard)
admin.site.register(Location)
admin.site.register(InventoryHistory)
admin.site.register(ForecastingPreferences)
admin.site.register(ForecastResults)
admin.site.register(DashboardReports)
admin.site.register(DashboardVisuals)
admin.site.register(ReportDateRange)
admin.site.register(UserDashSettings)
admin.site.register(OrderStatus)
admin.site.register(ReorderThreshold)
admin.site.register(Supplier)
admin.site.register(PurchaseOrder)
admin.site.register(Notifications)
admin.site.register(CustomerOrder)
admin.site.register(OrderItem)
admin.site.register(Shipment)
admin.site.register(AuditTrail)
admin.site.register(WorksOn)