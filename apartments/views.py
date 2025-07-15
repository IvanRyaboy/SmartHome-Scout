from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from .models import Apartment
from .forms import *


class ApartmentsHomeView(ListView):
    template_name = "apartments/apartments_list.html"
    model = Apartment
    context_object_name = 'apartments_list'


class FlatDetailView(DetailView):
    model = Apartment
    context_object_name = 'apartment'
    template_name = 'apartments/apartment_view.html'


class AddApartmentView(LoginRequiredMixin, CreateView):
    form_class = AddApartmentForm
    template_name = 'apartments/add_apartment.html'
    title_page = 'Добавление квартиры'

    def form_valid(self, form):
        f = form.save(commit=False)
        f.author = self.request.user
        return super().form_valid(form)
