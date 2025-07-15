from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView

from apartments.models import Apartment
from .models import *
from .forms import CustomUserCreationForm


class ProfilePageView(DetailView):
    model = get_user_model()
    context_object_name = 'user'
    template_name = 'account/profile_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['apartments'] = Apartment.objects.filter(owner=self.object)
        return context
