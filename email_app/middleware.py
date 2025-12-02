import json
import time
from django.utils.deprecation import MiddlewareMixin
from .models import APIRequestLog


class APILoggingMiddleware(MiddlewareMixin):
    """
    Middleware to log all API requests to the database.
    """
    
    def process_request(self, request):
        # Only log API endpoints
        if request.path.startswith('/api/'):
            request._start_time = time.time()
        return None
    
    def process_response(self, request, response):
        # Only log API endpoints
        if not request.path.startswith('/api/'):
            return response
        
        # Calculate response time
        if hasattr(request, '_start_time'):
            response_time = (time.time() - request._start_time) * 1000  # Convert to milliseconds
        else:
            response_time = 0
        
        # Get request data
        request_data = ''
        if request.method == 'POST':
            try:
                request_data = request.body.decode('utf-8')
            except Exception:
                request_data = '<binary data>'
        
        # Get IP address
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip_address = x_forwarded_for.split(',')[0]
        else:
            ip_address = request.META.get('REMOTE_ADDR')
        
        # Get user (may be None if authentication failed)
        user = getattr(request, 'user', None)
        if user and not user.is_authenticated:
            user = None
        
        # Create log entry
        try:
            APIRequestLog.objects.create(
                user=user,
                endpoint=request.path,
                method=request.method,
                request_data=request_data,
                response_status=response.status_code,
                response_time=response_time,
                ip_address=ip_address
            )
        except Exception as e:
            # Don't fail the request if logging fails
            print(f"Failed to log request: {e}")
        
        return response
