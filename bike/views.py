from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.contrib import messages
from django.views.generic.edit import FormView
from django.urls import reverse_lazy

from .enums import ComplaintStatus
from .forms import LoginForm, RegisterForm, EditProfileForm, ComplaintForm, ReservationForm
from .models import User, Complaint, Comment, Bike, Category


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


def bike_list(request):
    bikes = Bike.objects.all()
    return render(request, 'bike_list.html', {'bikes': bikes})


def bike_detail(request, slug):
    bike = get_object_or_404(Bike, slug=slug)
    return render(request, 'bike_detail.html', {'bike': bike})


def category_list(request):
    categories = Category.objects.all()
    return render(request, 'category_list.html', {'categories': categories})


def category_detail(request, pk):
    category = Category.objects.get(id=pk)
    bikes = Bike.objects.filter(categories=category)
    return render(request, 'category_detail.html', {'bikes': bikes})


def about(request):
    return render(request, 'about_us.html')


# ----------- #
# RESERVATION #
# ----------- #


class ReserveBikeView(FormView):
    template_name = 'reservation.html'
    form_class = ReservationForm
    success_url = reverse_lazy('home')

    def get_initial(self):
        bike_id = self.kwargs['bike_id']
        bike = Bike.objects.get(id=bike_id)
        return {'bike': bike}

    def form_valid(self, form):
        reservation = form.save(commit=False)
        reservation.user = self.request.user
        reservation.save()
        form.save_m2m()
        bike = form.cleaned_data['bike']
        bike.available = False
        bike.save()
        return super().form_valid(form)
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


def search(request):
    query = request.GET.get('q')
    bikes = Bike.objects.filter(description__contains=query)
    context = {'bikes': bikes}
    return render(request, 'search.html', context)
