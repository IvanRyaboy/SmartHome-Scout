from django.urls import path, reverse_lazy
from . import views


app_name = "apartments"

urlpatterns = [
    path('', views.ApartmentsHomeView.as_view(), name='home'),
    path('apartment/<uuid:pk>/', views.ApartmentDetailView.as_view(), name='apartment_detail'),
    path('add_apartment/', views.AddApartmentView.as_view(), name='add_apartment'),
    path('update_apartment/<uuid:pk>/', views.UpdateApartmentView.as_view(), name='update_apartment'),
    path('update_apartment/<uuid:pk>/delete/', views.DeleteApartmentView.as_view(), name='delete_apartment'),
]
