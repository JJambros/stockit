from django.contrib import admin
from .models import Profile, Inventory, Customer, Dashboard, Location, InventoryHistory, \
    ForecastingPreferences, ForecastResults, DashboardReports, DashboardVisuals, ReportDateRange, \
    UserDashSettings, OrderStatus, ReorderThreshold, Supplier, PurchaseOrder, Notifications, \
    CustomerOrder, OrderItem, Shipment, AuditTrail, WorksOn  # Import your models


# Base Admin class to handle soft deletion filtering and restoration
class SoftDeleteAdmin(admin.ModelAdmin):
    # Override the default queryset to filter out soft-deleted records
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(is_deleted=False)

    # Add an action to restore soft-deleted records
    def restore_records(self, request, queryset):
        queryset.update(is_deleted=False)
        self.message_user(request, "Selected records have been restored.")

    # Register the restore action
    actions = ['restore_records']


# Customized Admin class for CustomerOrder to handle AuditTrail and soft deletion
class CustomerOrderAdmin(SoftDeleteAdmin):
    def save_model(self, request, obj, form, change):
        obj.save()
        # Pass user to the signal when saving the model
        create_audit_trail_on_save(sender=CustomerOrder, instance=obj, created=not change, user=request.user)

    def delete_model(self, request, obj):
        # Soft delete the CustomerOrder instead of deleting it
        obj.is_deleted = True
        obj.save()
        # Optionally create an audit entry for soft deletion
        create_audit_trail_on_save(sender=CustomerOrder, instance=obj, created=False, user=request.user)


# Register your models with SoftDeleteAdmin or custom admin classes
admin.site.register(Profile, SoftDeleteAdmin)
admin.site.register(Inventory, SoftDeleteAdmin)
admin.site.register(Customer, SoftDeleteAdmin)
admin.site.register(Dashboard, SoftDeleteAdmin)
admin.site.register(Location, SoftDeleteAdmin)
admin.site.register(InventoryHistory, SoftDeleteAdmin)
admin.site.register(ForecastingPreferences, SoftDeleteAdmin)
admin.site.register(ForecastResults, SoftDeleteAdmin)
admin.site.register(DashboardReports, SoftDeleteAdmin)
admin.site.register(DashboardVisuals, SoftDeleteAdmin)
admin.site.register(ReportDateRange, SoftDeleteAdmin)
admin.site.register(UserDashSettings, SoftDeleteAdmin)
admin.site.register(OrderStatus, SoftDeleteAdmin)
admin.site.register(ReorderThreshold, SoftDeleteAdmin)
admin.site.register(Supplier, SoftDeleteAdmin)
admin.site.register(PurchaseOrder, SoftDeleteAdmin)
admin.site.register(Notifications, SoftDeleteAdmin)
admin.site.register(CustomerOrder, CustomerOrderAdmin)  # Use the customized admin for CustomerOrder
admin.site.register(OrderItem, SoftDeleteAdmin)
admin.site.register(Shipment, SoftDeleteAdmin)
admin.site.register(AuditTrail)  # No need for soft deletion, so default admin is fine
admin.site.register(WorksOn, SoftDeleteAdmin)
