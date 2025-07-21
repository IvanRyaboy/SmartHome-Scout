from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import *
from .views_api import *

app_name = "accounts"


router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')


urlpatterns = [
    path("profile/<uuid:pk>/", ProfilePageView.as_view(), name="profile")
] + router.urls
