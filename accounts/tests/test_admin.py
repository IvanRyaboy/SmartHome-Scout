import pytest
from django.contrib import admin
from django.contrib.auth import get_user_model

pytestmark = pytest.mark.django_db


def test_custom_user_registered_in_admin():
    User = get_user_model()
    assert User in admin.site._registry
    model_admin = admin.site._registry[User]
    assert hasattr(model_admin, "add_form")
    assert hasattr(model_admin, "form")
    assert isinstance(model_admin.list_display, (list, tuple))
    assert "username" in model_admin.list_display or "email" in model_admin.list_display
