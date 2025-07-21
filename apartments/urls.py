from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views
from . import views_api


app_name = "apartments"


router = DefaultRouter()
router.register(r'apartments', views_api.ApartmentViewSet, basename='apartment')
router.register(r'towns', views_api.TownViewSet, basename='town')
router.register(r'locations', views_api.LocationViewSet, basename='location')
router.register(r'buildings', views_api.BuildingViewSet, basename='building')


urlpatterns = [
    path('', views.ApartmentsHomeView.as_view(), name='home'),
    path('apartment/<uuid:pk>/', views.ApartmentDetailView.as_view(), name='apartment_detail'),
    path('add_apartment/', views.AddApartmentView.as_view(), name='add_apartment'),
    path('update_apartment/<uuid:pk>/', views.UpdateApartmentView.as_view(), name='update_apartment'),
    path('update_apartment/<uuid:pk>/delete/', views.DeleteApartmentView.as_view(), name='delete_apartment'),

    path('regions/', views_api.RegionAPIList.as_view()),
    path('regions/<int:pk>/', views_api.RegionAPIRetrieve.as_view()),
] + router.urls
