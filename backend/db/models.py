import random
from django.db import models
from datetime import datetime
from django.utils import timezone
from django.contrib.auth.models import User  # Importing the built-in    model
from django.contrib.contenttypes.models import ContentType # Store metadata about models installed in app (refer to any model in a generic way)
from django.contrib.contenttypes.fields import GenericForeignKey # Used to refer to any specific object of any model in app

# Create your models here.

# Profile model to store additional user information
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=1)  # Link Profile to User
    Fname = models.CharField(max_length=15)
    Minit = models.CharField(max_length=1, null=True, blank=True)
    Lname = models.CharField(max_length=15)
    email = models.EmailField(max_length=50, unique=True)  # Unique
    phone_number = models.CharField(max_length=20, unique=False)  # Unique
    is_deleted = models.BooleanField(default=False)  # Field for soft deletion

    def delete(self, using=None, keep_parents=False):
        """
        Override the delete method to implement soft deletion.
        Instead of deleting the profile, mark it as deleted.
        """
        self.is_deleted = True
        self.save()

    def restore(self):
        """
        Restore a soft-deleted profile by setting is_deleted to False.
        """
        self.is_deleted = False
        self.save()

    def __str__(self):
        return f'{self.Fname} {self.Lname}'

    @classmethod
    def active_profiles(cls):
        """
        Class method to filter only active (non-soft-deleted) profiles.
        """
        return cls.objects.filter(is_deleted=False)
    
# Category class to store information on categories
class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)
    is_deleted = models.BooleanField(default=False) # For soft deletion if needed

    def __str__(self):
        return self.name
    
# Inventory class to store information on inventory items
class Inventory(models.Model):
    inventory_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=15)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    forecast_level = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  # Link to Category
    is_deleted = models.BooleanField(default=False)  # New field for soft deletion

    def __str__(self):
        return self.name
    
# Customer class to store information on the customer (who orders FROM us)
class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    contact_fname = models.CharField(max_length=20)
    contact_lname = models.CharField(max_length=40)
    shipping_address = models.CharField(max_length=50)
    customer_email = models.EmailField(max_length=40, unique=True) # Unique
    customer_phone = models.CharField(max_length=20, unique=True) # Unique
    is_deleted = models.BooleanField(default=False)  # New field for soft deletion

    def __str__(self):
        return self.name

# Dashboard class to store information on the dashboard
class Dashboard(models.Model):
    dashboard_id = models.AutoField(primary_key=True)
    dashboard_type = models.CharField(max_length=20)
    key_metrics = models.CharField(max_length=20)
    last_updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)  # Link to the built-in User model
    is_deleted = models.BooleanField(default=False)  # New field for soft deletion

    def __str__(self):
        return self.dashboard_type

# Location model to store additional location info
class Location(models.Model):
    location_id = models.AutoField(primary_key=True)
    address = models.CharField(max_length=30)
    city = models.CharField(max_length=20)
    state = models.CharField(max_length=2)
    postal_code = models.CharField(max_length=5)
    is_deleted = models.BooleanField(default=False)  # New field for soft deletion

    def __str__(self):
        return f'{self.address}, {self.city}, {self.state}, {self.postal_code}'

# InventoryHistory model to store information about the inventory's history
class InventoryHistory(models.Model):
    history_id = models.AutoField(primary_key=True)
    transaction_date = models.DateTimeField(auto_now_add=True)  # Captures the exact time of the transaction
    
    TRANSACTION_TYPES = (
        ('sale', 'Sale'),
        ('restock', 'Restock'),
        ('return', 'Return'),
        ('adjustment', 'Adjustment'),
    )
    
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)  # Includes Sale, Restock, Return, Adjustment
    quantity = models.IntegerField()  # How much was sold or restocked (negative for returns)
    remaining_quantity = models.IntegerField()  # Updated inventory level after the transaction
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE)  # Link to Inventory
    source = models.CharField(max_length=100, blank=True, null=True)  # Source of transaction (e.g., order ID, shipment ID)
    is_deleted = models.BooleanField(default=False)  # New field for soft deletion
    
    def __str__(self):
        return f'{self.transaction_type} of {self.quantity} units on {self.transaction_date}'

# Supplier model to hold information about the Supplier
class Supplier(models.Model):
    supplier_id = models.AutoField(primary_key=True)
    supplier_name = models.CharField(max_length=50)
    contact_email = models.EmailField(max_length=50)
    contact_phone = models.CharField(max_length=20)
    is_deleted = models.BooleanField(default=False)  # New field for soft deletion

    def __str__(self):
        return self.supplier_name

# Supplier model to hold information about the Suppliers orders
class SupplierOrder(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    product = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    status = models.CharField(max_length=20, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.supplier} - {self.product} - {self.quantity}'

# ForecastingPreferences model to store information about the user's forecasting preferences
class ForecastingPreferences(models.Model):
    preference_id = models.AutoField(primary_key=True)
    forecast_time_range = models.CharField(max_length=50)
    desired_safety_stock = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    
    # New fields for extended forecasting options
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    trend_direction = models.CharField(max_length=10, choices=[('increase', 'Increase'), ('decrease', 'Decrease')], null=True, blank=True)
    trend_percent = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f'Forecasting Preferences for {self.user}'

# ForecastResults model to store information about the Forecasting Results
class ForecastResults(models.Model):
    forecast_id = models.AutoField(primary_key=True)
    forecast_date = models.DateField()
    forecast_quantity = models.IntegerField()
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE)  # Link to Inventory
    is_deleted = models.BooleanField(default=False)  # New field for soft deletion

    def __str__(self):
        return f'Forecast Result {self.forecast_id} for {self.inventory}'

# DashboardResults model to store information about the Dashboard's results
class DashboardReports(models.Model):
    report_id = models.AutoField(primary_key=True)
    report_type = models.CharField(max_length=50)
    generated_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    dashboard = models.ForeignKey(Dashboard, on_delete=models.CASCADE)  # Link to Dashboard
    is_deleted = models.BooleanField(default=False)  # New field for soft deletion

    def __str__(self):
        return f'Report {self.report_id} for {self.dashboard}'

# DashboardVisuals model to store information for the visuals in the dashboard
class DashboardVisuals(models.Model):
    visual_id = models.AutoField(primary_key=True)
    visual_type = models.CharField(max_length=50)
    data_source = models.CharField(max_length=50)
    date_range = models.CharField(max_length=50)
    dashboard = models.ForeignKey(Dashboard, on_delete=models.CASCADE)  # Link to Dashboard
    is_deleted = models.BooleanField(default=False)  # New field for soft deletion

    def __str__(self):
        return f'Visual {self.visual_id} for {self.dashboard}'

# ReportDateRange model to store information on the date range
class ReportDateRange(models.Model):
    date_range_id = models.AutoField(primary_key=True)
    report_type = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()
    dashboard = models.ForeignKey(Dashboard, on_delete=models.CASCADE)  # Link to Dashboard
    is_deleted = models.BooleanField(default=False)  # New field for soft deletion

    def __str__(self):
        return f'Report Date Range {self.date_range_id} for {self.dashboard}'

# UserDashSettings model to store information on the users' settings for the dashboard
class UserDashSettings(models.Model):
    setting_id = models.AutoField(primary_key=True)
    preferred_visuals = models.CharField(max_length=50)
    default_report_type = models.CharField(max_length=50)
    default_date_range = models.CharField(max_length=50)
    dashboard = models.ForeignKey(Dashboard, on_delete=models.CASCADE)  # Link to Dashboard
    is_deleted = models.BooleanField(default=False)  # New field for soft deletion

    def __str__(self):
        return f'Settings {self.setting_id} for {self.dashboard}'

# Orderstatus model to store information on the status of the order
class OrderStatus(models.Model):
    PROCESSING = 'processing'
    SHIPPED = 'shipped'
    DELIVERED = 'delivered'

    STATUS_CHOICES = (
        (PROCESSING, 'Processing'),
        (SHIPPED, 'Shipped'),
        (DELIVERED, 'Delivered'),
    )

    current_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PROCESSING)

    status_id = models.AutoField(primary_key=True)
    is_deleted = models.BooleanField(default=False)  # New field for soft deletion

    def __str__(self):
        return f'Status {self.status_id}'

    # ReorderThreshold model to hold information on the threshold for a reorder
class ReorderThreshold(models.Model):
    threshold_id = models.AutoField(primary_key=True)
    reorder_point = models.IntegerField()
    reorder_quantity = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)  # Link to User
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, default=1)  # New field for Supplier
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE)  # Link to Inventory
    is_deleted = models.BooleanField(default=False)  # New field for soft deletion

    def __str__(self):
        return f'Reorder Threshold {self.threshold_id} for {self.inventory}'

# PurchaseOrder model to hold information about the Purchase Order
class PurchaseOrder(models.Model):
    po_id = models.AutoField(primary_key=True)
    order_quantity = models.IntegerField()
    po_date = models.DateField()
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)  # Link to Supplier
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE)  # Link to Inventory
    is_deleted = models.BooleanField(default=False)  # New field for soft deletion

    def __str__(self):
        return f'Purchase Order {self.po_id} from {self.supplier}'

# Notification model to hold information for notifications
class Notifications(models.Model):
    notification_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)  # Link to User
    message = models.TextField()
    is_deleted = models.BooleanField(default=False)  # New field for soft deletion

    def __str__(self):
        return f'Notification {self.notification_id} for {self.user}'

# CustomerOrder model to hold information about a customer's order
class CustomerOrder(models.Model):
    order_id = models.AutoField(primary_key=True)
    from_company = models.CharField(max_length=20)
    to_company = models.CharField(max_length=20)
    customer_order_date = models.DateField()
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    status = models.ForeignKey(OrderStatus, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)  # Add this line to link to the user
    is_deleted = models.BooleanField(default=False)  # New field for soft deletion
    shipped = models.BooleanField(default=False)  # To mark when the item is ready for shipment

    def update_status_to_shipped(self):
        if self.shipped:
            self.status.current_status = OrderStatus.SHIPPED
            self.status.save()

    def mark_as_delivered(self):
        self.status.current_status = OrderStatus.DELIVERED
        self.status.save()

    def __str__(self):
        return f'Customer Order {self.order_id} from {self.from_company} to {self.to_company}'

# OrderItem model to hold information about the item in the order
class OrderItem(models.Model):
    order_item_id = models.AutoField(primary_key=True)
    quantity = models.IntegerField()
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE)  # Link to Inventory
    order = models.ForeignKey(CustomerOrder, on_delete=models.CASCADE)  # Link to CustomerOrder
    is_deleted = models.BooleanField(default=False)  # New field for soft deletion

    def __str__(self):
        return f'Order Item {self.order_item_id} for Order {self.order}'
    
# Shipment model to hold information about shipping
class Shipment(models.Model):
    shipment_id = models.AutoField(primary_key=True)
    tracking_number = models.CharField(max_length=20, default="0000")  # Default tracking number
    shipping_company = models.CharField(max_length=100, default="To Be Determined")  # Default company name
    shipped_date = models.DateField()
    est_delivery_date = models.DateField()
    order = models.ForeignKey(CustomerOrder, on_delete=models.CASCADE)  # Link to CustomerOrder
    is_deleted = models.BooleanField(default=False)  # New field for soft deletion

    def save(self, *args, **kwargs):
        # Generate a random 9-digit tracking number if not already set
        if not self.tracking_number or self.tracking_number == "0000":
            while True:
                new_tracking_number = f"{random.randint(100000000, 999999999)}"
                if not Shipment.objects.filter(tracking_number=new_tracking_number).exists():
                    self.tracking_number = new_tracking_number
                    break
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Shipment {self.shipment_id} for Order {self.order}'

class AuditTrail(models.Model):
    audit_id = models.AutoField(primary_key=True)
    change_time = models.DateTimeField(auto_now_add=True)
    changed_by = models.ForeignKey(User, on_delete=models.CASCADE)
    changed_desc = models.CharField(max_length=255)

    content_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True)  # Track the model type
    object_id = models.CharField(max_length=255, null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')  # Link to any model
    is_deleted = models.BooleanField(default=False)  # New field for soft deletion

    def __str__(self):
        return f'Change by {self.changed_by} at {self.change_time} - {self.changed_desc}'

    
# WorksOn model -- needed to represent a many-to-many relationship
class WorksOn(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)  # Link to User
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE)  # Link to Inventory
    order = models.ForeignKey(CustomerOrder, on_delete=models.CASCADE)  # Link to CustomerOrder
    is_deleted = models.BooleanField(default=False)  # New field for soft deletion
    
    class Meta:
        unique_together = (('user', 'inventory', 'order'),)  # Ensures unique combination of these fields

# Notification model to hold information for notifications
class Notifications(models.Model):
    notification_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)  # Link to User
    message = models.TextField()
    is_deleted = models.BooleanField(default=False)  # New field for soft deletion


    def __str__(self):
        return f'Notification {self.notification_id} for {self.user}'

   # ReorderThreshold model to hold information on the threshold for a reorder
class ReorderThreshold(models.Model):
    threshold_id = models.AutoField(primary_key=True)
    reorder_point = models.IntegerField()
    reorder_quantity = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)  # Link to User
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, default=1)  # New field for Supplier
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE)  # Link to Inventory
    is_deleted = models.BooleanField(default=False)  # New field for soft deletion


    def __str__(self):
        return f'Reorder Threshold {self.threshold_id} for {self.inventory}'

