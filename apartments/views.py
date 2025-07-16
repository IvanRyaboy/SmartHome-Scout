from django.contrib.auth.mixins import LoginRequiredMixin
from django_filters.views import FilterView

from .utils import OwnerRequiredMixin
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Apartment
from .forms import *
from .filters import ApartmentFilter


class ApartmentsHomeView(FilterView):
    template_name = "apartments/apartments_list.html"
    model = Apartment
    paginate_by = 10
    filterset_class = ApartmentFilter


class FlatDetailView(DetailView):
    model = Apartment
    context_object_name = 'apartment'
    template_name = 'apartments/apartment_view.html'


class AddApartmentView(LoginRequiredMixin, CreateView):
    form_class = AddApartmentForm
    template_name = 'apartments/add_apartment.html'
    title_page = 'Create apartment'

    def form_valid(self, form):
        apartment = form.save(commit=False, owner=self.request.user)

        apartment.save()

        images = self.request.FILES.getlist('image')
        for img in images:
            ApartmentImage.objects.create(apartment=apartment, image=img)

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title_page'] = self.title_page
        return context


class UpdateApartmentView(LoginRequiredMixin, OwnerRequiredMixin, UpdateView):
    model = Apartment
    form_class = AddApartmentForm
    template_name = 'apartments/add_apartment.html'

    def get_success_url(self):
        return self.object.get_absolute_url()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context

    def form_valid(self, form):
        images = self.request.FILES.getlist('image')
        for img in images:
            ApartmentImage.objects.create(apartment=self.object, image=img)
        return super().form_valid(form)


class DeleteApartmentView(LoginRequiredMixin, OwnerRequiredMixin, DeleteView):
    model = Apartment

    def get_success_url(self):
        return reverse('apartments:home')
