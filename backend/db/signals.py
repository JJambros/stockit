from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from crum import get_current_user  # Import from crum to get the current user context
from .models import CustomerOrder, AuditTrail

@receiver(post_save, sender=CustomerOrder)
def create_audit_trail_on_save(sender, instance, created, **kwargs):
    user = get_current_user()  # Use crum to get the current user context
    action = "Created" if created else "Updated"
    
    # Handle case where user might not be available
    AuditTrail.objects.create(
        order=instance,
        changed_by=user if user and user.is_authenticated else None,  # Ensure 'user' is not null
        changed_desc=f"{action} customer order"
    )

@receiver(post_delete, sender=CustomerOrder)
def create_audit_trail_on_delete(sender, instance, **kwargs):
    user = get_current_user()  # Use crum to get the user performing the delete action
    if user and user.is_authenticated:
        AuditTrail.objects.create(
            order=None,  # Set order to None since it's being deleted
            changed_by=user,  # Set the user who made the change
            changed_desc="Deleted customer order"
        )
