from django.urls import path

from .views import *

app_name = "accounts"


urlpatterns = [
    path("profile/<uuid:pk>/", ProfilePageView.as_view(), name="profile")
]
