from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import Role, AuditLog

CustomUser = get_user_model()


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = [
        'email',
        'username',
        'role',
        'is_staff',
        'is_superuser',
    ]
    list_filter = ['role', 'is_staff', 'is_superuser']
    fieldsets = UserAdmin.fieldsets + (('Role', {'fields': ('role',)}),)
    add_fieldsets = UserAdmin.add_fieldsets + (('Role', {'fields': ('role',)}),)
    filter_horizontal = UserAdmin.filter_horizontal


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ['id', 'table_name', 'record_id', 'action', 'timestamp', 'user_id']
    list_filter = ['action', 'table_name']
    search_fields = ['record_id', 'table_name']
    readonly_fields = ['user_id', 'timestamp', 'table_name', 'record_id', 'action', 'old_values', 'new_values']
    date_hierarchy = 'timestamp'


admin.site.register(CustomUser, CustomUserAdmin)
