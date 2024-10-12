class AuditTrailMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Example: Capture GET or POST requests and log them
        if request.method in ['POST', 'PUT', 'DELETE']:
            # Log the request details to AuditTrail
            AuditTrail.objects.create(
                changed_by=request.user if request.user.is_authenticated else None,
                changed_desc=f"Action: {request.method} on {request.path}"
            )

        return response
