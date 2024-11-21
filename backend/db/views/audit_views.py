from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.shortcuts import render # Needed for audit-trail
from ..models import AuditTrail
from ..serializers import AuditTrailSerializer


# --------- AUDIT TRAIL VIEWS --------- #

@api_view(['GET'])
@permission_classes([AllowAny])
def audit_trail_list(request):
    audit_trails = AuditTrail.objects.all()  # No need to filter by 'is_deleted' if AuditTrail is permanent
    serializer = AuditTrailSerializer(audit_trails, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def audit_log_view(request):
    audit_logs = AuditTrail.objects.all().order_by('-change_time')
    return render(request, 'audit_log.html', {'audit_logs': audit_logs})
