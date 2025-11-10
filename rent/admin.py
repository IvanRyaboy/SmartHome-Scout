from django.contrib import admin
from .models import Rent, IDS


@admin.register(Rent)
class RentAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    ordering = ['title']


@admin.register(IDS)
class IDSAdmin(admin.ModelAdmin):
    list_display = ('rent_id', 'status')

