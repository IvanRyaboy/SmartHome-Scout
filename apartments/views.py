from django.contrib.auth.mixins import LoginRequiredMixin
from django_filters.views import FilterView

from .mixins import OwnerRequiredMixin
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Apartment
from .forms import *
from .filters import ApartmentFilter
from .utils import create_apartment_with_images, update_apartment_images


class ApartmentsHomeView(FilterView):
    template_name = "apartments/apartments_list.html"
    model = Apartment
    paginate_by = 10
    filterset_class = ApartmentFilter


class ApartmentDetailView(DetailView):
    model = Apartment
    context_object_name = 'apartment'
    template_name = 'apartments/apartment_view.html'


class AddApartmentView(LoginRequiredMixin, CreateView):
    form_class = AddApartmentForm
    template_name = 'apartments/add_apartment.html'
    title_page = 'Create apartment'

    def form_valid(self, form):
        create_apartment_with_images(owner=self.request.user, form=form, files=self.request.FILES)
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
        self.object = form.save()
        update_apartment_images(apartment=self.object, files=self.request.FILES)
        return super().form_valid(form)


class DeleteApartmentView(LoginRequiredMixin, OwnerRequiredMixin, DeleteView):
    model = Apartment

    def get_success_url(self):
        return reverse('apartments:home')
