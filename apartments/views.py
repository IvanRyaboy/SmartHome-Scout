from django.shortcuts import render
from django.views.generic import ListView


class ApartmentsHome(ListView):
    template_name = "apartments/index.html"
