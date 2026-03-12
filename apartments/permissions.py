from rest_framework import permissions


class IsOwnerOrAdmin(permissions.BasePermission):
    """Allow owner, staff, or users with administrator/moderator role."""
    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False
        if obj.owner == request.user:
            return True
        if getattr(request.user, 'is_staff', False):
            return True
        if getattr(request.user, 'is_administrator_role', False):
            return True
        if getattr(request.user, 'is_moderator_role', False):
            return True
        return False
