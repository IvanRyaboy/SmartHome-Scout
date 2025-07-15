from django.urls import path, reverse_lazy
from . import views


app_name = "apartments"

urlpatterns = [
    path('', views.ApartmentsHomeView.as_view(), name='home'),
    path('flat/<uuid:pk>/', views.FlatDetailView.as_view(), name='flat_detail'),
    path('add_apartment/', views.AddApartmentView.as_view(), name='add_apartment'),
]
