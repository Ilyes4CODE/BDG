from rest_framework.response import Response
from rest_framework import status
from functools import wraps
from django.contrib.auth.decorators import login_required

def group_required(group_name):
    """
    Decorator to verify if the user belongs to a specific group.
    :param group_name: Name of the required group
    :return: The view if the user has the group, otherwise Forbidden
    """
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def _wrapped_view(request, *args, **kwargs):
            # Check if the user belongs to the required group
            if request.user.groups.filter(name=group_name).exists():
                return view_func(request, *args, **kwargs)
            else:
                return Response("You do not have permission to access this resource.",status=status.HTTP_401_UNAUTHORIZED )
        return _wrapped_view
    return decorator
