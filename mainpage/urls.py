from django.urls import path
from .views import *


urlpatterns = [
    path("", HomePageView.as_view(), name='home'),
    path("about/", AboutPageView.as_view(), name='about'),
    path("property/", PropertyPageView.as_view(), name='property'),
    path('webhook-endpoint/', receive_webhook, name='receive_webhook'),
]
