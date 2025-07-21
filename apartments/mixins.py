from django.http import HttpResponseForbidden


class OwnerRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.owner != self.request.user:
            return HttpResponseForbidden("Access denied")
        return super().dispatch(request, *args, **kwargs)
