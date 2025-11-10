from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views_api


app_name = "rent"


router = DefaultRouter()
router.register(r'rent', views_api.RentViewSet, basename='rent')

urlpatterns = [

] + router.urls
