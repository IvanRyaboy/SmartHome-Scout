from django.urls import path, reverse_lazy
from . import views


app_name = "apartments"

urlpatterns = [
    path('', views.ApartmentsHomeView.as_view(), name='home'),
]
