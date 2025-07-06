from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('pending-users/', views.pending_users, name='pending_users'),
    path('approve-user/<int:user_id>/', views.approve_user, name='approve_user'),
] 