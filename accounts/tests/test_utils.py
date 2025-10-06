import pytest
from django.http import HttpResponseForbidden
from django.contrib.auth import get_user_model
from django.views.generic import DetailView

from accounts.utils import OwnerRequiredMixin

pytestmark = pytest.mark.django_db


class DummyView(OwnerRequiredMixin, DetailView):
    model = get_user_model()


def test_owner_required_forbids_when_user_is_not_owner(rf, user):
    other = get_user_model().objects.create_user(
        username="other", email="other@example.com", password="pass123"
    )

    request = rf.get("/profile/")
    request.user = other

    view = DummyView()
    view.request = request
    view.kwargs = {"pk": user.pk}
    view.get_object = lambda: user

    resp = view.dispatch(request)
    assert isinstance(resp, HttpResponseForbidden)
    assert resp.status_code == 403


def test_owner_required_allows_owner(rf, user):
    request = rf.get("/profile/")
    request.user = user

    view = DummyView()
    view.request = request
    view.kwargs = {"pk": user.pk}
    view.get_object = lambda: user

    resp = view.dispatch(request)
    assert not isinstance(resp, HttpResponseForbidden)
