from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth import login
from .forms import CustomUserCreationForm
from .models import CustomUser

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Registration successful! Please wait for admin approval.')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.is_staff)
def pending_users(request):
    pending_users = CustomUser.objects.filter(is_approved=False)
    return render(request, 'users/pending_users.html', {'pending_users': pending_users})

@login_required
@user_passes_test(lambda u: u.is_staff)
def approve_user(request, user_id):
    user = CustomUser.objects.get(id=user_id)
    user.is_approved = True
    user.save()
    messages.success(request, f'User {user.username} has been approved.')
    return redirect('pending_users')

def is_approved_user(user):
    return user.is_approved
