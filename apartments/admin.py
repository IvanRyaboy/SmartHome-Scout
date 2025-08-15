from django.contrib import admin
from .models import *


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    ordering = ['name']


@admin.register(Town)
class TownAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    ordering = ['name']


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('id', 'town')
    list_display_links = ('id', 'town')


@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):
    list_display = ('id', 'location')
    list_display_links = ('id', 'location')


@admin.register(Apartment)
class ApartmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'building')
    list_display_links = ('id', 'building')


@admin.register(ApartmentImage)
class ApartmentImageAdmin(admin.ModelAdmin):
    pass


@admin.register(IDS)
class IDSAdmin(admin.ModelAdmin):
    pass
