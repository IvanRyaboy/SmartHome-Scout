import pytest
from django.contrib.auth import get_user_model
from accounts.forms import CustomUserCreationForm, CustomUserChangeForm

pytestmark = pytest.mark.django_db


def test_custom_user_creation_form_valid_creates_user():
    form = CustomUserCreationForm(
        data={
            "username": "newuser",
            "email": "new@example.com",
            "password1": "StrongPass123!",
            "password2": "StrongPass123!",
        }
    )
    assert form.is_valid(), form.errors
    user = form.save()
    assert user.pk
    assert user.email == "new@example.com"


def test_custom_user_change_form_updates_fields(user):
    form = CustomUserChangeForm(
        data={"username": "upd", "email": "upd@example.com"},
        instance=user,
    )
    assert form.is_valid(), form.errors
    updated = form.save()
    assert updated.username == "upd"
    assert updated.email == "upd@example.com"
