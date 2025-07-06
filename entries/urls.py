from django.urls import path
from . import views

urlpatterns = [
    path('entry/create/', views.entry_create, name='entry_create'),
    path('entry/list/', views.entry_list, name='entry_list'),
    path('entry/<int:pk>/edit/', views.entry_edit, name='entry_edit'),
    path('entry/<int:pk>/calculate-interest/', views.calculate_interest, name='calculate_interest'),
    path('entry/<int:pk>/release/', views.release_entry, name='release_entry'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/released-entries/', views.released_entries, name='released_entries'),
    path('admin/export/', views.export_to_excel, name='export_to_excel'),
] 