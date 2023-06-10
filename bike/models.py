from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from .enums import *
import uuid
import datetime
from django.core.exceptions import ValidationError


def validate_positive_number(value):
    if value <= 0:
        raise ValidationError(
            _("%(value)s is not a positive number"),
            params={"value": value},
        )

class User(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    credit = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    def is_worker(self):
        return self.groups.filter(name='worker').exists()

    def is_mechanic(self):
        return self.groups.filter(name='mechanic').exists()


class Category(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, unique=True)
    image = models.ImageField(upload_to='categories/')

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Bike(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category = models.ForeignKey(Category, related_name='bike', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    year = models.PositiveSmallIntegerField(default=2000)
    owner = models.CharField(max_length=255, default='admin')
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='bikes/')
    slug = models.SlugField(max_length=255)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    in_stock = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    ip_address = models.GenericIPAddressField(protocol='IPv4', null=True, blank=True )

    def __str__(self):
        return self.name


class Reservation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bike = models.ForeignKey(Bike, on_delete=models.CASCADE)
    requestDate = models.DateTimeField(default=now)
    endDate = models.DateTimeField()
    status = models.CharField(
        _('status'), default=ReservationStatus.PENDING.name, choices=ReservationStatus.choices(), max_length=32
    )

    def __str__(self):
        return str(self.bike.name) +\
               ' [' + str(self.requestDate.strftime('%Y-%m-%d %H:%m')) + ']'


class Complaint(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    lastUpdate = models.DateTimeField(default=now)
    customer = models.ForeignKey(User, related_name='customer_complaint', on_delete=models.CASCADE)
    worker = models.ForeignKey(User, related_name='worker_complaint', on_delete=models.SET_NULL, null=True)
    mechanic = models.ForeignKey(User, related_name='mechanic_complaint', on_delete=models.SET_NULL, null=True)
    description = models.CharField(max_length=256)
    status = models.CharField(
        _('status'), default=ComplaintStatus.UNATTACHED.name, choices=ComplaintStatus.choices(), max_length=32
    )

    class Meta:
        ordering = ['-lastUpdate']

    def __str__(self):  
        return self.customer.username + ' (' + str(self.id) + ')'


class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    content = models.TextField()
    time = models.DateTimeField(default=now)
    complaint = models.ForeignKey(Complaint, related_name='comment', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='comment', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username + ' (' + str(self.id) + ')'


# return a date when the invoice is expired
def invoice_due_to():
        return now() + datetime.timedelta(days=1)

class Invoice(models.Model):
    user = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE)
    created_on = models.DateTimeField('created on', default=now)
    paid_on = models.DateTimeField('paid on', null=True, blank=True)
    due_date = models.DateTimeField('due date', default=invoice_due_to)
    amount = models.DecimalField(max_digits=6, decimal_places=2, default=50, validators=[validate_positive_number])
    status = models.CharField(
        _('status'), default=InvoiceStatus.UNPAID.name, choices=InvoiceStatus.choices(), max_length=32
    )
    paid_via = models.TextField(default='Stripe')
    comment = models.TextField(null=True, blank=True)

    def __str__(self):
        return 'Invoice #' + str(self.id) + ' (' + self.user.username + ')'


class Location(models.Model):
    bike = models.ForeignKey(Bike, related_name='bike', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=now)
    latitude = models.FloatField(null=False, blank=False)  #pos[0], float
    longitude = models.FloatField(null=False, blank=False) #pos[1], float
    altitude = models.FloatField(null=False, blank=False) #alt, float
    speed  = models.FloatField(null=False, blank=False) #speed, float
    track = models.IntegerField(null=False, blank=False)#track, int
    climb  = models.FloatField(null=False, blank=False) #climb, float
    time  = models.DateTimeField(null=False, blank=False) #time, datetime.datetime
    error_horizontal = models.FloatField(null=False, blank=False) #precision[0], float
    error_vertical = models.FloatField(null=False, blank=False) #precision[1], float

    def __str__(self):
        return 'Location #' + str(self.id) + ' (' + self.bike.name + ')'

class BikeStatus(models.Model):
    bike = models.ForeignKey(Bike, on_delete=models.CASCADE)
    time = models.DateTimeField(default=now)
    is_online = models.BooleanField()
    is_locked = models.BooleanField()

    def __str__(self):
        return 'BikeStatus #' + str(self.id) + ' (' + self.bike.name + ')'
