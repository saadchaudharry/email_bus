import base64
from functools import wraps
from django.http import JsonResponse
from django.contrib.auth import authenticate
from .models import APIToken


def api_auth_required(view_func):
    """
    Decorator to require either Token or Basic authentication.
    
    Token Auth: Authorization: Token <token>
    Basic Auth: Authorization: Basic <base64(username:password)>
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        
        if not auth_header:
            return JsonResponse({'error': 'Authentication required'}, status=401)
        
        # Token Authentication
        if auth_header.startswith('Token '):
            token = auth_header.replace('Token ', '')
            try:
                api_token = APIToken.objects.get(token=token)
                request.user = api_token.user
                return view_func(request, *args, **kwargs)
            except APIToken.DoesNotExist:
                return JsonResponse({'error': 'Invalid token'}, status=401)
        
        # Basic Authentication
        elif auth_header.startswith('Basic '):
            try:
                encoded_credentials = auth_header.replace('Basic ', '')
                decoded_credentials = base64.b64decode(encoded_credentials).decode('utf-8')
                username, password = decoded_credentials.split(':', 1)
                
                user = authenticate(username=username, password=password)
                if user is not None:
                    request.user = user
                    return view_func(request, *args, **kwargs)
                else:
                    return JsonResponse({'error': 'Invalid credentials'}, status=401)
            except Exception:
                return JsonResponse({'error': 'Invalid authentication format'}, status=401)
        
        else:
            return JsonResponse({'error': 'Unsupported authentication method'}, status=401)
    
    return wrapper
