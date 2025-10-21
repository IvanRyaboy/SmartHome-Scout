from django.urls import path
from .views import *


urlpatterns = [
    path("", HomePageView.as_view(), name='home'),
    path("about/", AboutPageView.as_view(), name='about'),
    path("property/", PropertyPageView.as_view(), name='property'),
    path('apartments-webhook-endpoint/', receive_apartments_webhook, name='receive_apartments_webhook'),
    path('rent-webhook-endpoint/', receive_rent_webhook, name='receive_rent_webhook')
]
