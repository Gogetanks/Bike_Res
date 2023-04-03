from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import LoginForm, RegisterForm, EditProfileForm
from .models import User


# ---- #
# HOME #
# ---- #
def home_request(request):
    return render(request, 'base.html')


# ------- #
# PROFILE #
# ------- #
def profile_request(request, username):
    if not request.user.is_authenticated:
        return redirect('login')

    user = User.objects.get(username=username)
    return render(request, 'accounts/profile.html', context={'user': user})


def edit_profile_request(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile', request.user.username)
    else:
        form = EditProfileForm(instance=request.user)
    return render(request, 'accounts/edit_profile.html', {'form': form})

# -------- #
# ACCOUNTS #
# -------- #
def login_request(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username_or_email = form.cleaned_data['username_or_email']
            password = form.cleaned_data['password']
            user = authenticate(username=username_or_email, password=password)
            if user is None:
                user = authenticate(email=username_or_email, password=password)
            if user is not None:
                login(request, user)
                return redirect('profile', user.username)
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', context={"form": form})


def logout_request(request):
    logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect('home')


def register_request(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.save()

            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', context={'form': form})

def delete_account_request(request):
    if request.method == 'GET':
        request.user.delete()
        return redirect('login')


def bikes(request):
    return HttpResponse("Bikes")


def about(request):
    return render(request, 'about_us.html')


def reserve(request):
    return render(request, 'reservation.html')


def payment(request):
    return render(request, 'payment.html')


def complaint(request):
    return render(request, 'complaint.html')

