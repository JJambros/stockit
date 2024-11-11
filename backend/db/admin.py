from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Profile, Inventory, Customer, Dashboard, ReorderThreshold, Location, InventoryHistory, \
    ForecastingPreferences, ForecastResults, DashboardReports, DashboardVisuals, ReportDateRange, \
    UserDashSettings, OrderStatus, ReorderThreshold, Supplier, PurchaseOrder, Notifications, \
    CustomerOrder, OrderItem, Shipment, AuditTrail, WorksOn, Category, SupplierOrder  # Import your models
from .signals import create_audit_trail

# Define a custom filter for the is_deleted field
class IsDeletedFilter(admin.SimpleListFilter):
    title = _('Deleted status')  # Display name for the filter in the admin interface
    parameter_name = 'is_deleted'  # URL parameter for the filter

    def lookups(self, request, model_admin):
        return (
            ('active', _('Active')),
            ('deleted', _('Deleted')),
            ('all', _('All')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'active':
            return queryset.filter(is_deleted=False)
        elif self.value() == 'deleted':
            return queryset.filter(is_deleted=True)
        return queryset  # Show all records if 'All' is selected or no filter is set


class SoftDeleteAdmin(admin.ModelAdmin):
    list_filter = (IsDeletedFilter,)  # Include the custom filter for deleted status

    # Override the default queryset to allow filtering by deleted status
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Apply filter based on the IsDeletedFilter's current setting
        filter_value = request.GET.get('is_deleted')
        if filter_value == 'active':
            return qs.filter(is_deleted=False)
        elif filter_value == 'deleted':
            return qs.filter(is_deleted=True)
        return qs  # Show all records if 'All' is selected or no filter is applied

    # Add an action to restore soft-deleted records
    def restore_records(self, request, queryset):
        queryset.update(is_deleted=False)
        self.message_user(request, "Selected records have been restored.")

    # Override the delete method to set `is_deleted=True` instead of deleting
    def delete_model(self, request, obj):
        obj.is_deleted = True  # Set is_deleted to True to soft delete
        obj.save()

    # Override the delete action to perform a soft delete on each selected item
    def delete_queryset(self, request, queryset):
        queryset.update(is_deleted=True)  # Perform a bulk update for soft delete

    # Register the restore action
    actions = ['restore_records']


# Customized Admin class for CustomerOrder to handle AuditTrail and soft deletion
class CustomerOrderAdmin(SoftDeleteAdmin):
    def save_model(self, request, obj, form, change):
        obj.save()
        # Use create_audit_trail directly instead
        create_audit_trail(obj, 'Created' if not change else 'Updated', request.user)

    def delete_model(self, request, obj):
        obj.is_deleted = True
        obj.save()
        # Use create_audit_trail for soft deletion
        create_audit_trail(obj, 'Soft Deleted', request.user)


# Register your models with SoftDeleteAdmin or custom admin classes
admin.site.register(Profile, SoftDeleteAdmin)
admin.site.register(Category, SoftDeleteAdmin)
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
admin.site.register(SupplierOrder, SoftDeleteAdmin)
admin.site.register(PurchaseOrder, SoftDeleteAdmin)
admin.site.register(Notifications, SoftDeleteAdmin)
admin.site.register(CustomerOrder, CustomerOrderAdmin)  # Use the customized admin for CustomerOrder
admin.site.register(OrderItem, SoftDeleteAdmin)
admin.site.register(Shipment, SoftDeleteAdmin)
admin.site.register(AuditTrail)  # No need for soft deletion, so default admin is fine
admin.site.register(WorksOn, SoftDeleteAdmin)

