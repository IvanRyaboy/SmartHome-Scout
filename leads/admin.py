from django.contrib import admin
from .models import Lead


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'listing_type', 'status', 'created_at']
    list_filter = ['listing_type', 'status']
    search_fields = ['contact_info', 'message']
    readonly_fields = ['created_at']
