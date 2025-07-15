from django.http import HttpResponseForbidden


class OwnerRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.owner != request.user:
            return HttpResponseForbidden("Доступ запрещён")
        return super().dispatch(request, *args, **kwargs)