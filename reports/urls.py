from django.urls import path
from . import views

app_name = "reports"

urlpatterns = [
    path('query-builder/', views.query_builder, name='query_builder'),
    path('query-builder/run/', views.query_builder_run, name='query_builder_run'),
    path('query-builder/export/', views.query_export_excel, name='query_export_excel'),
]
