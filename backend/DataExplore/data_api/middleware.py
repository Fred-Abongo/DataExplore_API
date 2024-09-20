from django.http import JsonResponse 
from django.core.exceptions import PermissionDenied
import logging

logger = logging.getLogger(__name__)

class CustomExceptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)
            return response
        except PermissionDenied as e:
            logger.error(f"Permission denied: {str(e)}")
            return JsonResponse({'error': 'Permission denied'}, status=403)
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return JsonResponse({'error': 'Internal server error'}, status=500)
