from django.contrib.auth.mixins import LoginRequiredMixin
from .utils import OwnerRequiredMixin
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
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
        f.owner = self.request.user
        return super().form_valid(form)


class UpdateApartmentView(LoginRequiredMixin, OwnerRequiredMixin, UpdateView):
    model = Apartment
    form_class = AddApartmentForm
    template_name = 'apartments/add_apartment.html'

    def get_success_url(self):
        return self.object.get_absolute_url()

    def get_context_data(self, request, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = request.user
        return context


class DeleteApartmentView(LoginRequiredMixin, OwnerRequiredMixin, DeleteView):
    model = Apartment

    def get_success_url(self):
        return reverse('apartments:home')
