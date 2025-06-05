from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
from django.http import JsonResponse

from .forms import LoginForm, RegisterForm

def get_tokens_for_user(user):
    """Generate JWT tokens for a user"""
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

def login_view(request):
    """Handle user login and redirect based on user type"""
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('/admin/')
        return redirect('/')
    
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)
                
                # Generate JWT tokens
                # tokens = get_tokens_for_user(user)yy
                tokens = get_tokens_for_user(user)
                
                # Set JWT token as a cookie
                response = redirect('/admin/' if user.is_superuser else '/')
                response.set_cookie(
                    'access_token',
                    tokens['access'],
                    max_age=3600,  # 1 hour
                    httponly=True,
                    samesite='Lax'
                )
                
                messages.success(request, f'Welcome back, {username}!')
                return response
            else:
                messages.error(request, 'Authentication failed. Please check your credentials.')
        else:
            pass
    else:
        form = LoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})

def register_view(request):
    """Handle user registration"""
    if request.user.is_authenticated:
        return redirect('/')
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('accounts:login')
    else:
        form = RegisterForm()
    
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def logout_view(request):
    """Handle user logout"""
    logout(request)
    response = redirect('/')
    response.delete_cookie('access_token')
    messages.success(request, 'You have been logged out successfully.')
    return response

@login_required
def profile_view(request):
    """Display user profile"""
    return render(request, 'accounts/profile.html')

@login_required
def user_reviews_view(request):
    """Display all reviews by the current user"""
    reviews = request.user.reviews.all().select_related('product')
    return render(request, 'accounts/user_reviews.html', {'reviews': reviews})
