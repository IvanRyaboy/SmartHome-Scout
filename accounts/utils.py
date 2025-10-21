from django.http import HttpResponseForbidden
from django.conf import settings
from django.contrib.auth import get_user_model


User = get_user_model()


class OwnerRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.pk != self.request.user.pk:
            return HttpResponseForbidden("Access denied")
        return super().dispatch(request, *args, **kwargs)


def get_service_user() -> User:
    user_id = getattr(settings, 'SERVICE_USER_ID', None)
    if user_id:
        return User.objects.get(id=user_id)
    return User.objects.filter(is_active=True, is_superuser=True).order_by('id').first()
