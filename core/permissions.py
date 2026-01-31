from rest_framework import permissions

class IsManager(permissions.BasePermission):
    """
    Allows access only to users in the 'Manager' group or superusers.
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return request.user.is_superuser or request.user.groups.filter(name='Manager').exists()

class IsStaff(permissions.BasePermission):
    """
    Allows access to any Staff member (including Managers).
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        # Assuming 'Staff' group exists, or simply check is_staff flag
        return request.user.is_staff or request.user.groups.filter(name='Staff').exists()
