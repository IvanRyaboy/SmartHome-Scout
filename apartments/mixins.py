from django.http import HttpResponseForbidden


class OwnerRequiredMixin:
    """Allow owner, staff, or users with administrator/moderator role."""
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.owner == request.user:
            return super().dispatch(request, *args, **kwargs)
        if getattr(request.user, 'is_staff', False):
            return super().dispatch(request, *args, **kwargs)
        if getattr(request.user, 'is_administrator_role', False):
            return super().dispatch(request, *args, **kwargs)
        if getattr(request.user, 'is_moderator_role', False):
            return super().dispatch(request, *args, **kwargs)
        return HttpResponseForbidden("Access denied")
