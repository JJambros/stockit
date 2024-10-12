# signals.py

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import CustomerOrder, AuditTrail

@receiver(post_save, sender=CustomerOrder)
def create_audit_trail_on_save(sender, instance, created, **kwargs):
    # Automatically create an AuditTrail entry for creation or update
    user = kwargs.get('user', None)  # Get the user from the kwargs
    if created:
        action = "Created"
    else:
        action = "Updated"
    
    AuditTrail.objects.create(
        order=instance,
        changed_by=user,  # Use the user from the view context
        changed_desc=f"{action} customer order"
    )

@receiver(post_delete, sender=CustomerOrder)
def create_audit_trail_on_delete(sender, instance, **kwargs):
    # Automatically create an AuditTrail entry for deletion
    user = kwargs.get('user', None)  # Get the user from the kwargs
    AuditTrail.objects.create(
        order=instance,
        changed_by=user,  # Ensure 'user' is available in the context
        changed_desc="Deleted customer order"
    )
