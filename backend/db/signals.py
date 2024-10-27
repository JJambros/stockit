from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from crum import get_current_user  # Import from crum to get the current user context
from django.contrib.contenttypes.models import ContentType
from .models import AuditTrail, OrderItem, PurchaseOrder, Inventory,  InventoryHistory

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
    action = "Created" if created else "Updated"
    create_audit_trail(instance, action, user)

@receiver(post_delete)
def track_changes_on_delete(sender, instance, **kwargs):
    user = get_current_user()  # Use crum to get the current user context
    create_audit_trail(instance, "Deleted", user)

# --------- SIGNAL FOR INVENTORY ADJUSTING --------- #

# Decrease inventory quantity when an OrderItem is created
@receiver(post_save, sender=OrderItem)
def decrease_inventory_on_order(sender, instance, created, **kwargs):
    if created:  # Only decrease if a new OrderItem is created
        inventory_item = instance.inventory
        
        # Decrease the quantity only once
        if not hasattr(inventory_item, '_quantity_updated'):
            inventory_item.quantity -= instance.quantity
            inventory_item.save(update_fields=['quantity'])
            inventory_item._quantity_updated = True  # Mark as updated to prevent multiple saves


# Increase inventory quantity when a PurchaseOrder is created
@receiver(post_save, sender=PurchaseOrder)
def increase_inventory_on_purchase(sender, instance, created, **kwargs):
    if created:  # Only increase if a new PurchaseOrder is created
        inventory_item = instance.inventory
        
        # Increase the quantity only once
        if not hasattr(inventory_item, '_quantity_updated'):
            inventory_item.quantity += instance.order_quantity
            inventory_item.save(update_fields=['quantity'])
            inventory_item._quantity_updated = True  # Mark as updated to prevent multiple saves


# --------- SIGNAL FOR INVENTORY_HISTORY --------- #

# Update inventory history when orders are sold
@receiver(post_save, sender=OrderItem)
def update_inventory_history_on_order(sender, instance, created, **kwargs):
    if created:
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
    if created:
        inventory = instance.inventory
        restock_quantity = instance.order_quantity  # Quantity restocked in this purchase order

        # Create a new entry in InventoryHistory for the restock
        InventoryHistory.objects.create(
            inventory=inventory,
            transaction_type='restock',
            quantity=restock_quantity,
            remaining_quantity=inventory.quantity + restock_quantity
        )
