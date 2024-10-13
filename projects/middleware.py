# projects/middleware.py

from django.http import JsonResponse

class IsAuthenticatedMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:
            return JsonResponse({"detail": "Authentication credentials were not provided."}, status=401)
        return self.get_response(request)
