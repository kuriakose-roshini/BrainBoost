# Admin/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomAdminRegistrationForm, CustomAdminLoginForm

def home(request):

    return render(request, "Admin/home.html")

def admin_register(request):
    """
    View for admin registration
    """
    if request.method == 'POST':
        form = CustomAdminRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('admin_dashboard')
    else:
        form = CustomAdminRegistrationForm()
    return render(request, 'Admin/admin_register.html', {'form': form})


def admin_login(request):
    """
    View for admin login
    """
    if request.method == 'POST':
        form = CustomAdminLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None and user.is_staff and user.is_superuser:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                return redirect('admin_dashboard')
            else:
                messages.error(request, 'Invalid credentials or unauthorized access.')
    else:
        form = CustomAdminLoginForm()
    return render(request, 'Admin/admin_login.html', {'form': form})


@login_required
def admin_dashboard(request):
    """
    Admin dashboard view
    """
    if not (request.user.is_staff and request.user.is_superuser):
        messages.error(request, 'Unauthorized access!')
        return redirect('admin_login')
    return render(request, 'Admin/admin_dashboard.html')


def admin_logout(request):
    """
    Admin logout view
    """
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('admin_login')


@login_required
def admin_profile(request):
    """
    Admin profile view
    """
    return render(request, 'admin/profile.html')