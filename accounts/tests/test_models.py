import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

pytestmark = pytest.mark.django_db


def test_custom_user_pk_is_uuid(user):
    assert user.pk and isinstance(user.pk.hex, str) and len(user.pk.hex) == 32


def test_get_absolute_url(user):
    expected = reverse("accounts:profile", args=[str(user.pk)])
    assert user.get_absolute_url() == expected
