from rest_framework.permissions import BasePermission

class GroupRequiredPermission(BasePermission):
    """
    Custom permission to check if the user is in a specific group.
    """
    def __init__(self, group_name):
        self.group_name = group_name

    def has_permission(self, request, view):
        # Check if the user is authenticated and belongs to the required group
        return request.user and request.user.is_authenticated and request.user.groups.filter(name=self.group_name).exists()
