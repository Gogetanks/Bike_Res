from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.contrib import messages

from .enums import ComplaintStatus
from .forms import LoginForm, RegisterForm, EditProfileForm, ComplaintForm
from .models import User, Complaint, Comment


# ----- #
# UTILS #
# ----- #
def get_user(request):
    if not request.user.is_authenticated:
        messages.error(request, 'You are must login to perform some actions.')
        return None
    return User.objects.get(username=request.user.username)

def get_worker(request):
    user = get_user(request)
    if not user:
        return None
    if not user.is_worker():
        messages.error(request, 'You are nor authorize to perform this action.')
        return None
    return User.objects.get(username=request.user.username)


# ---- #
# HOME #
# ---- #
def home_request(request):
    return render(request, 'base.html')


# ------- #
# PROFILE #
# ------- #
def profile_request(request):
    user = get_user(request)
    if not user:
        return redirect('login')

    if user.is_worker():
        return render(request, 'accounts/worker_profile.html', context={'user': user})

    return render(request, 'accounts/base_profile.html', context={'user': user})


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
                return redirect('profile')
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
    user = get_user(request)
    if not user:
        return redirect('login')

    if request.method == 'GET':
        user.delete()
        return redirect('login')


# -------- #
#  WORKER  #
# -------- #
def worker_main_request(request):
    user = get_user(request)
    if not user:
        return redirect('login')

    if user.is_worker():
        return render(request, 'worker/worker_main.html')
    return redirect('home')


def account_management_request(request):
    user = get_user(request)
    if not user:
        return redirect('login')

    if user.is_worker():
        users = User.objects.all()
        groups = Group.objects.all()
        return render(request, 'worker/account_management.html', {'users': users, 'groups': groups})
    return redirect('home')


def deactivate_user(request, user_id):
    user = get_user(request)
    if not user:
        return redirect('login')

    if user.is_worker():
        user = User.objects.get(id=user_id)
        user.is_active = False
        user.save()
    return redirect('account_management')


def delete_user(request, user_id):
    user = get_user(request)
    if not user:
        return redirect('login')

    if user.is_worker():
        user = User.objects.get(id=user_id)
        user.delete()
    return redirect('account_management')


def bikes(request):
    return HttpResponse("Bikes")


def about(request):
    return render(request, 'about_us.html')


def reserve(request):
    return render(request, 'reservation.html')


def payment(request):
    return render(request, 'payment.html')


# ---------- #
# COMPLAINTS #
# ---------- #
def complaints_request(request):
    user = get_user(request)
    if not user:
        return redirect('login')

    if user.is_worker():
        return render(request, 'complaints/base_complaints.html',
                      {'complaints': Complaint.objects.filter(worker=user)})

    return render(request, 'complaints/customer_complaints.html',
                  {'complaints': Complaint.objects.filter(customer=user)})


def unattached_complaints_request(request):
    worker = get_worker(request)
    if not worker:
        return redirect('complaints')

    return render(request, 'complaints/unattached_complaints.html',
                  {'complaints': Complaint.objects.filter(status='UNATTACHED')})


def complaint_request(request, complaint_id):
    user = get_user(request)
    if not user:
        return redirect('login')

    if (user.is_worker() and not Complaint.objects.filter(worker=user, id=complaint_id).exists())\
            and not Complaint.objects.filter(customer=user, id=complaint_id).exists():
        messages.error(request, 'Invalid complaint')
        return redirect('complaints')

    complaint = Complaint.objects.get(id=complaint_id)
    return render(request, 'complaints/complaint.html',
                  {'complaint': complaint,
                   'comments': Comment.objects.filter(complaint=complaint)})


def new_complaint_request(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        form = ComplaintForm(request.POST)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.customer = request.user
            complaint.save()
            comment = Comment(content=complaint.description, complaint=complaint, user=request.user)
            comment.save()

            return redirect('complaint', complaint.id)
    else:
        form = ComplaintForm()
    return render(request, 'complaints/new_complaint.html', {'form': form})


def take_complaint_request(request, complaint_id):
    worker = get_worker(request)
    if worker:
        complaint = Complaint.objects.get(id=complaint_id)
        complaint.worker = worker
        complaint.status = ComplaintStatus.OPENED.name
        complaint.save()

    return redirect('complaints')
