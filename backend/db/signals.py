from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from crum import get_current_user  # Import from crum to get the current user context
from django.utils import timezone # For Tracking Shipping
from datetime import timedelta # For Tracking Shipping
from threading import Timer # For Tracking Shipping
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from .models import AuditTrail, SupplierOrder, SalesOrderItem, PurchaseOrder, Inventory, ReorderThreshold, InventoryHistory, UserProfile, SalesOrderShipment


# --------- SIGNAL FOR AUDIT TRAIL --------- #

def create_audit_trail(instance, action, user):
    # Get the content type for the model (ensure it exists)
    content_type = ContentType.objects.get_for_model(instance)

    # Prevent recursion: Do not create an audit trail for the AuditTrail model itself
    if content_type.model == 'audittrail':
        return  # Avoid recursion by exiting when the model is AuditTrail

    # If the user is not authenticated or None, skip creating an audit trail
    if not user or not user.is_authenticated:
        return  # Skipping the audit trail when user is not available or authenticated

    # Create the AuditTrail entry
    AuditTrail.objects.create(
        content_type=content_type,  # Set the content type of the model
        object_id=instance.pk,  # Set the specific instance of the model
        changed_by=user,  # Set the user who made the change
        changed_desc=f"{action} {content_type.model}"
    )

@receiver(post_save)
def track_changes_on_save(sender, instance, created, **kwargs):
    user = get_current_user()  # Use crum to get the current user context
    if hasattr(instance, 'is_deleted') and instance.is_deleted:
        action = "Soft Deleted"
    else:
        action = "Created" if created else "Updated"
    create_audit_trail(instance, action, user)

@receiver(pre_delete)
def track_changes_on_soft_delete(sender, instance, **kwargs):
    if hasattr(instance, 'is_deleted') and not instance.is_deleted:
        user = get_current_user()  # Use crum to get the current user context
        instance.is_deleted = True  # Soft delete the item
        instance.save()
        create_audit_trail(instance, "Soft Deleted", user)


# --------- SIGNAL FOR INVENTORY ADJUSTING --------- #

# Decrease inventory quantity when an OrderItem is created
@receiver(post_save, sender=SalesOrderItem)
def decrease_inventory_on_order(sender, instance, created, **kwargs):
    if created and not instance.inventory.is_deleted:  # Only decrease if a new OrderItem is created and not soft-deleted
        inventory_item = instance.inventory
        
        # Decrease the quantity only once
        if not hasattr(inventory_item, '_quantity_updated'):
            inventory_item.quantity -= instance.quantity
            inventory_item.save(update_fields=['quantity'])
            inventory_item._quantity_updated = True  # Mark as updated to prevent multiple saves


# Increase inventory quantity when a PurchaseOrder is created
@receiver(post_save, sender=PurchaseOrder)
def increase_inventory_on_purchase(sender, instance, created, **kwargs):
    if created and not instance.inventory.is_deleted:  # Only increase if a new PurchaseOrder is created and not soft-deleted
        inventory_item = instance.inventory
        
        # Increase the quantity only once
        if not hasattr(inventory_item, '_quantity_updated'):
            inventory_item.quantity += instance.order_quantity
            inventory_item.save(update_fields=['quantity'])
            inventory_item._quantity_updated = True  # Mark as updated to prevent multiple saves

@receiver(post_save, sender=Inventory)
def auto_generate_order(sender, instance, **kwargs):
    try:
        # Retrieve the reorder threshold for this inventory item
        threshold = ReorderThreshold.objects.get(inventory=instance)

        # Check if the inventory quantity is below the reorder point
        if instance.quantity < threshold.reorder_point:
            SupplierOrder.objects.create(
                supplier=threshold.supplier,  # Adjust if needed to get the relevant supplier
                product=instance,
                quantity=threshold.reorder_quantity  # Quantity to reorder from the threshold
            )
    except ReorderThreshold.DoesNotExist:
        # Log or handle the case where no reorder threshold is set for this inventory item
        print(f"No reorder threshold set for Inventory item: {instance.name}")

# --------- SIGNAL FOR INVENTORY_HISTORY --------- #

# Update inventory history when orders are sold
@receiver(post_save, sender=SalesOrderItem)
def update_inventory_history_on_order(sender, instance, created, **kwargs):
    if created and not instance.inventory.is_deleted:  # Only update if the inventory is not soft-deleted
        inventory = instance.inventory
        sold_quantity = instance.quantity  # Quantity sold in this order item
        
        # Create a new entry in InventoryHistory for the sale
        InventoryHistory.objects.create(
            inventory=inventory,
            transaction_type='sale',
            quantity=sold_quantity,
            remaining_quantity=inventory.quantity - sold_quantity
        )

@receiver(post_save, sender=PurchaseOrder)
def update_inventory_history_on_restock(sender, instance, created, **kwargs):
    if created and not instance.inventory.is_deleted:  # Only update if the inventory is not soft-deleted
        inventory = instance.inventory
        restock_quantity = instance.order_quantity  # Quantity restocked in this purchase order

        # Create a new entry in InventoryHistory for the restock
        InventoryHistory.objects.create(
            inventory=inventory,
            transaction_type='restock',
            quantity=restock_quantity,
            remaining_quantity=inventory.quantity + restock_quantity
        )


# --------- SIGNAL FOR PROFILE --------- #

# Should create a profile automatically when a user is created.
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        # Create a new profile if the user is created
        UserProfile.objects.create(
            user=instance,
            Fname=instance.first_name if instance.first_name else "FirstName",
            Lname=instance.last_name if instance.last_name else "LastName",
            email=instance.email if instance.email else f"{instance.username}@example.com", # Fill in just for a profile creation, can be changed manually
            phone_number="0000000000" # Fill in just for a profile creation, can be changed manually
        )
    else:
        # Update the profile if the user is updated
        UserProfile.objects.filter(user=instance).update(
            Fname=instance.first_name,
            Lname=instance.last_name,
            email=instance.email
        )

# --------- SIGNAL FOR TRACKING SHIPPING --------- #

@receiver(post_save, sender=SalesOrderItem)
def create_shipment_on_order_item(sender, instance, created, **kwargs):
    if created:
        # Calculate the shipment and estimated delivery dates
        shipped_date = timezone.now().date()
        est_delivery_date = shipped_date + timedelta(days=1)

        # Create the Shipment automatically
        SalesOrderShipment.objects.create(
            order=instance.order,
            shipped_date=shipped_date,
            est_delivery_date=est_delivery_date
        )