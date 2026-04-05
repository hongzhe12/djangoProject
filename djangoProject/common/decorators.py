# common/decorators.py
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.http import JsonResponse

def require_jwt(view_func):
    def wrapper(request, *args, **kwargs):
        auth = JWTAuthentication()
        try:
            user, token = auth.authenticate(request)
            request.user = user
        except Exception:
            return JsonResponse({'code': 401, 'message': 'Invalid token'}, status=401)
        return view_func(request, *args, **kwargs)
    return wrapper