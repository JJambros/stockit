from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from crum import get_current_user  # Import from crum to get the current user context
from django.contrib.contenttypes.models import ContentType
from .models import AuditTrail

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
