from django.contrib import admin
from .models import Rent


@admin.register(Rent)
class RentAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    ordering = ['title']
