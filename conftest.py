import pytest
from django.contrib.auth import get_user_model
from allauth.account.models import EmailAddress


@pytest.fixture
def user(db):
    """
    Базовый пользователь без подтверждённого email.
    """
    User = get_user_model()
    return User.objects.create_user(
        username="testuser",
        email="user@example.com",
        password="pass123"
    )


@pytest.fixture
def verified_user(db):
    """
    Пользователь с подтверждённым email (для сценариев,
    где allauth требует верификации).
    """
    User = get_user_model()
    user = User.objects.create_user(
        username="verified",
        email="verified@example.com",
        password="pass123"
    )
    EmailAddress.objects.create(
        user=user,
        email=user.email,
        verified=True,
        primary=True,
    )
    return user


@pytest.fixture
def auth_client(client, verified_user):
    """
    Django test client, авторизованный под verified_user.
    Удобно для API и view-тестов.
    """
    client.force_login(verified_user)
    return client


@pytest.fixture
def superuser(db):
    """
    Суперпользователь для тестов админки или сценариев с правами.
    """
    User = get_user_model()
    return User.objects.create_superuser(
        username="admin",
        email="admin@example.com",
        password="adminpass"
    )
