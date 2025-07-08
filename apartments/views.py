from django.shortcuts import render
from django.views.generic import ListView
from .models import Apartment


class ApartmentsHomeView(ListView):
    template_name = "apartments/apartments_list.html"
    queryset = Apartment
