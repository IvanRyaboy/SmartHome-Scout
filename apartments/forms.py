from django import forms
from .models import *


class AddApartmentForm(forms.ModelForm):
    class Meta:
        model = Apartment
        fields = '__all__'
        exclude = ['owner']
