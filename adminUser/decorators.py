from functools import wraps
from django.shortcuts import redirect

def check_superadmin():
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if getattr(request.user, "is_staff", None) == True:
                return view_func(request, *args, **kwargs)
            return redirect("home")
        return _wrapped_view
    return decorator