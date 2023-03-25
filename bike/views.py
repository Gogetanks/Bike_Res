from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import LoginForm, RegisterForm
from .models import User

# ---- #
# HOME #
# ---- #
def home_request(request):
    return HttpResponse("Hello, world!")


# ------- #
# PROFILE #
# ------- #
def profile_request(request, username):
    if not request.user.is_authenticated:
        return redirect('login')

    user = User.objects.get(username=username)
    return render(request, 'accounts/profile.html', context={'user': user})


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
        print("Errors?")
        if form.is_valid():
            print("NO")
            user = form.save()
            user.save()

            return redirect('login')
        print("YES")
    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', context={'form': form})
