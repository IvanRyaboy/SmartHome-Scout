from django.http import HttpResponseForbidden


class OwnerRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.pk != self.request.user.pk:
            return HttpResponseForbidden("Access denied")
        return super().dispatch(request, *args, **kwargs)
