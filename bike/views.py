from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.contrib import messages
from django.views.generic.edit import FormView
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView

from .enums import ComplaintStatus, InvoiceStatus, ReservationStatus
from .forms import LoginForm, RegisterForm, EditProfileForm, ComplaintForm, ReservationForm, TopUpForm
from .models import User, Complaint, Comment, Bike, Category, Invoice, Reservation
from django.utils.timezone import now
from decimal import Decimal

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
    if not user.is_worker() and not user.is_mechanic():
        messages.error(request, 'You are not authorized to perform this action.')
        return None
    return User.objects.get(username=request.user.username)

def get_mechanic(request):
    user = get_user(request)
    if not user:
        return None
    if not user.is_mechanic() and not user.is_worker():
        messages.error(request, 'You are not authorized to perform this action.')
        return None
    return User.objects.get(username=request.user.username)


# ---- #
# HOME #
# ---- #
def home_request(request):
    featured_bikes = Bike.objects.filter(is_featured=True)
    context = {'featured_bikes': featured_bikes}
    return render(request, 'home.html', context)


# ------- #
# PROFILE #
# ------- #
def profile_request(request):
    user = get_user(request)
    if not user:
        return redirect('login')

    return render(request, 'accounts/base_profile.html', context={'user': user})


def edit_profile_request(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
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
            messages.success(request, "Your account has been successfully created.")
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

def topup_account_request(request):
    if request.method == 'POST':
        form = TopUpForm(request.POST)
        if form.is_valid():
            #invoice = Invoice(user=request.user, amount=form.cleaned_data['amount'], comment='TopUp account #{id}'.format(id=request.user.id))
            #invoice.save()
            invoice = form.save(commit=False)
            invoice.user = request.user
            invoice.comment='TopUp account #{id}'.format(id=request.user.id)
            invoice.save()
            return redirect('invoice', invoice.id)
    else:
        form = TopUpForm()
    return render(request, 'accounts/topup_account.html', {'form': form})

# MECHANIC

def mechanic_main_request(request):
    user = get_user(request)
    if not user:
        return redirect('login')

    if user.is_mechanic():
        return render(request, 'mechanic/mechanic_main.html')
    return redirect('home')

# -------- #
#  WORKER  #
# -------- #
def worker_main_request(request):
    if not get_worker(request):
        return redirect('login')

    return render(request, 'worker/worker_main.html')

def account_management_request(request):
    user = get_user(request)
    if not user:
        return redirect('login')

    if user.is_worker():
        users = User.objects.all()
        groups = Group.objects.all()
        return render(request, 'worker/account_management.html', {'users': users, 'groups': groups})
    return redirect('home')


def invoice_management_request(request):
    if request.user.is_worker():
        invoices = Invoice.objects.all()
        return render(request, 'worker/invoice_management.html', {'invoices': invoices})
    return redirect('home')

def worker_pay_invoice(request, invoice_id):
    if request.user.is_worker():
        invoice = Invoice.objects.get(id=invoice_id)
        if (invoice.status == InvoiceStatus.UNPAID.name) and (invoice.due_date > now()):
            invoice.status = InvoiceStatus.PAID.name
            invoice.paid_on = now()
            invoice.save()
            if "TopUP" in invoice.comment:
                user = User.objects.get(id=invoice.user.id)
                user.credit += invoice.amount
                user.save()
            if "Reservation" in invoice.comment:
                start_index = invoice.comment.find("Reservation ID:") + len("Reservation ID:")
                end_index = invoice.comment.find(",", start_index)
                reservation_id = invoice.comment[start_index:end_index].strip()
                reservation = get_object_or_404(Reservation, id=reservation_id)
                reservation.status = ReservationStatus.FINISHED.name
                reservation.save()
                messages.success(request, 'Reservation payment successful with store credit.')

        else:
            messages.error(request, 'You are only allowed to pay an UNEXPIRED invoice with status UNPAID')
        return redirect('invoice_management')
    else:
        messages.error(request, 'You must be authorized to browse the requested page')
        return redirect('home')

def cancel_invoice(request, invoice_id):
    invoice = Invoice.objects.get(id=invoice_id)
    def cancel_routine():
        if invoice.status == InvoiceStatus.UNPAID.name:
            invoice.status = InvoiceStatus.CANCELED.name
            invoice.save()
        else:
            messages.error(request, 'You are only allowed to cancel an invoice with status UNPAID')
    if request.user.is_worker():
        cancel_routine()
        return redirect('invoice_management')
    if not request.user.is_authenticated:
        messages.error(request, 'You must be authorized to browse the requested page')
        return redirect('login')
    if not Invoice.objects.filter(user=request.user, id=invoice_id).exists():
        messages.error(request, 'You are not allowed to browse the requested page')
        return redirect('invoices')
    else:
        cancel_routine()
        return redirect('invoices')

def delete_invoice(request, invoice_id):
    invoice = Invoice.objects.get(id=invoice_id)
    def delete_routine():
        if invoice.status != InvoiceStatus.PAID.name:
            invoice.delete()
        else:
            messages.error(request, 'You are not allowed to delete an invoice with status PAID')
    if request.user.is_worker():
        delete_routine()
        return redirect('invoice_management')
    if not request.user.is_authenticated:
        messages.error(request, 'You must be authorized to browse the requested page')
        return redirect('login')
    if not Invoice.objects.filter(user=request.user, id=invoice_id).exists():
        messages.error(request, 'You are not allowed to browse the requested page')
        return redirect('invoices')
    else:
        delete_routine()
        return redirect('invoices')


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

def reservations_request(request):
    if not get_worker(request):
        return redirect('login')

    reservations = Reservation.objects.all()
    return render(request, 'worker/reservations.html', {'reservations': reservations})

# ----- #
# ABOUT #
# ----- #


def about(request):
    return render(request, 'about_us.html')

# ----------------------#
#  BIKES AND CATEGORIES #
# --------------------- #


def bike_list(request):
    bikes = Bike.objects.all()
    return render(request, 'bike_list.html', {'bikes': bikes})


def bike_detail(request, slug):
    bike = get_object_or_404(Bike, slug=slug)
    return render(request, 'bike_detail.html', {'bike': bike})


def category_list(request):
    categories = Category.objects.all()
    return render(request, 'category_list.html', {'categories': categories})


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    bikes = Bike.objects.filter(category=category)
    return render(request, 'category_detail.html', {'bikes': bikes})


# ------ #
# SEARCH #
# ------ #


def search(request):
    query = request.GET.get('q')
    bikes = Bike.objects.filter(description__contains=query)
    context = {'bikes': bikes}
    return render(request, 'search.html', context)


# ----------- #
# RESERVATION #
# ----------- #


class ReserveBikeView(FormView):
    template_name = 'reservation.html'
    model = Reservation
    form_class = ReservationForm
    success_url = reverse_lazy('home')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)

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
        # Calculate the total price
        start_date = reservation.requestDate
        end_date = reservation.endDate
        price = bike.price
        total_price = price * (end_date - start_date).days

        # Redirect to the reservation summary page with the necessary data
        return redirect(reverse('reservation_summary', kwargs={'pk': reservation.pk}))


class ReservationSummaryView(DetailView):
    model = Reservation
    template_name = 'reservation_summary.html'
    context_object_name = 'reservation'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Calculate duration in days and total price
        reservation = self.object
        duration = (reservation.endDate - reservation.requestDate).days
        total_price = duration * reservation.bike.price

        context['duration'] = duration
        context['total_price'] = total_price

        return context

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

    if user.is_mechanic():
        return render(request, 'complaints/base_complaints.html',
                      {'complaints': Complaint.objects.filter(mechanic=user)})

    return render(request, 'complaints/customer_complaints.html',
                  {'complaints': Complaint.objects.filter(customer=user)})


def unattached_complaints_request(request):
    worker = get_worker(request)
    mechanic = get_mechanic(request)
    if not worker or not mechanic:
        return redirect('complaints')

    return render(request, 'complaints/unattached_complaints.html',
                  {'complaints': Complaint.objects.filter(status='UNATTACHED')})


def complaint_request(request, complaint_id):
    user = get_user(request)
    if not user:
        return redirect('login')

    complaint = Complaint.objects.get(id=complaint_id)

    if request.method == 'POST':
        if 'newMessage' in request.POST:
            newMessage = request.POST['newMessage']
            if newMessage:
                newComment = Comment.objects.create(content=newMessage, complaint=complaint, user=user)
                complaint.lastUpdate = newComment.time
                complaint.save()

        if 'newMechanic' in request.POST:
            print(request.POST['newMechanic'])
            newMechanic = User.objects.get(id=request.POST['newMechanic'])
            complaint.mechanic = newMechanic
            complaint.save()
            messages.success(request, 'Mechanic ' + newMechanic.username + ' has been added to the chat.')

    if (user.is_worker() and not Complaint.objects.filter(worker=user, id=complaint_id).exists())\
            and not Complaint.objects.filter(customer=user, id=complaint_id).exists():
        messages.error(request, 'Invalid complaint')
        return redirect('complaints')

    if user.is_worker():
        return render(request, 'complaints/worker_complaint.html',
                      {'complaint': complaint,
                       'comments': Comment.objects.filter(complaint=complaint),
                       'user': user,
                       'mechanics': User.objects.filter(groups__name='mechanic')})

    if user.is_mechanic():
        return render(request, 'complaints/worker_complaint.html',
               {'complaint': complaint,
                'comments': Comment.objects.filter(complaint=complaint),
                'user': user})

    return render(request, 'complaints/base_complaint.html',
                  {'complaint': complaint,
                   'comments': Comment.objects.filter(complaint=complaint),
                   'user': user})


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
    mechanic = get_mechanic(request)
    if worker:
        complaint = Complaint.objects.get(id=complaint_id)
        complaint.worker = worker
        complaint.status = ComplaintStatus.OPENED.name
        complaint.save()
    if mechanic:
        complaint = Complaint.objects.get(id=complaint_id)
        complaint.mechanic = mechanic
        complaint.status = ComplaintStatus.OPENED.name
        complaint.save()
    return redirect('complaints')


def solve_complaint_request(request, complaint_id):
    worker = get_worker(request)
    mechanic = get_mechanic(request)
    if worker or mechanic:
        complaint = Complaint.objects.get(id=complaint_id)
        complaint.status = ComplaintStatus.SOLVED.name
        complaint.save()

    return redirect('complaint', complaint_id)


def reopen_complaint_request(request, complaint_id):
    user = get_user(request)
    if user:
        complaint = Complaint.objects.get(id=complaint_id)
        complaint.status = ComplaintStatus.OPENED.name
        complaint.save()

    return redirect('complaint', complaint_id)


def payment(request):
    return render(request, 'payment.html')
def make_credit_payment(request, reservation_id):
    if not request.user.is_authenticated:
        return redirect('login')

    reservation = get_object_or_404(Reservation, id=reservation_id)
    user = get_user(request)
    duration = (reservation.endDate - reservation.requestDate).days
    total_price = duration * reservation.bike.price

    if reservation.user == user:
        use_store_credit = request.POST.get('use_store_credit', True)

        if use_store_credit:
            if user.credit >= total_price:
                # Deduct the price from the user's store credit
                user.credit -= reservation.bike.price
                user.save()
                # Update the reservation status as paid
                reservation.status = ReservationStatus.FINISHED.name
                reservation.save()
                messages.success(request, 'Reservation payment successful with store credit.')
                return redirect('profile')
            else:
                reservation.delete()
                messages.error(request, 'Insufficient store credit. Please choose another payment method.')
                return redirect('topup_account')

    return redirect('profile')

def make_card_payment(request, reservation_id):
    if not request.user.is_authenticated:
        return redirect('login')

    reservation = get_object_or_404(Reservation, id=reservation_id)
    user = get_user(request)
    duration = (reservation.endDate - reservation.requestDate).days
    total_price = duration * reservation.bike.price

    if reservation.user == user:
        use_store_credit = request.POST.get('use_store_credit', False)

        if not use_store_credit:
            # Generate the invoice
            invoice = Invoice()
            invoice.user = user
            invoice.comment = 'Reservation ID: {id}, Bike: {bike}'.format(id=reservation.id, bike=reservation.bike.name)
            invoice.save()
            return redirect('invoice', invoice.id)

    return redirect('profile')

# ---------- #
#  INVOICES  #
# ---------- #
def invoices_request(request):
    if not request.user.is_authenticated:
        return redirect('login')

    return render(request, 'invoices/invoices.html',
                  {'invoices': Invoice.objects.filter(user=request.user)})


def invoice_request(request, invoice_id):
    if not request.user.is_authenticated:
        return redirect('login')

    if (not Invoice.objects.filter(user=request.user, id=invoice_id).exists()) and (not request.user.is_worker()):
        messages.error(request, 'You are not allowed to see that page')
        return redirect('invoices')

    invoice = Invoice.objects.get(id=invoice_id)
    return render(request, 'invoices/invoice.html',
                  {'invoice': invoice,
                   })
