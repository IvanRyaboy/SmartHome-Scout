import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

pytestmark = pytest.mark.django_db


def test_profile_requires_login(client, user):
    url = reverse("accounts:profile", args=[str(user.pk)])
    resp = client.get(url)
    assert resp.status_code in (302, 301)
    assert "login" in resp.headers.get("Location", "").lower()


def test_profile_forbidden_for_other_user(client, user):
    other = get_user_model().objects.create_user(
        username="other", email="other@example.com", password="pass123"
    )
    client.force_login(other)
    url = reverse("accounts:profile", args=[str(user.pk)])
    resp = client.get(url)
    assert resp.status_code == 403


def test_profile_ok_for_owner(auth_client, verified_user):
    url = reverse("accounts:profile", args=[str(verified_user.pk)])
    resp = auth_client.get(url)
    assert resp.status_code == 200
    assert "user" in resp.context
    assert resp.context["user"].pk == verified_user.pk


def test_profile_context_apartments_filtered(monkeypatch, auth_client, verified_user):
    """
    Изолируемся от реальной модели Apartment:
    подменяем accounts.views.Apartment.objects.filter и проверяем вызов с owner=self.object.
    """
    calls = {}

    class DummyManager:
        @staticmethod
        def filter(**kwargs):
            calls["kwargs"] = kwargs
            return ["apt1", "apt2"]

    class DummyApartment:
        objects = DummyManager()

    import accounts.views as views_mod
    monkeypatch.setattr(views_mod, "Apartment", DummyApartment, raising=True)

    url = reverse("accounts:profile", args=[str(verified_user.pk)])
    resp = auth_client.get(url)

    assert resp.status_code == 200
    assert calls["kwargs"] == {"owner": verified_user}
    assert resp.context["apartments"] == ["apt1", "apt2"]
