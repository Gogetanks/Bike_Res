from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from .enums import *
import uuid

class User(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)

    def is_worker(self):
        return self.groups.filter(name='worker').exists()

    def is_mechanic(self):
        return self.groups.filter(name='mechanic').exists()

class Category(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, unique=True)

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
    description = models.TextField()
    image = models.ImageField(upload_to='images/')
    slug = models.SlugField(max_length=255)
    price = models.DecimalField(max_digits=4, decimal_places=2)
    in_stock = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Reservation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bikes = models.ManyToManyField(Bike)
    requestDate = models.DateTimeField(default=now)
    endDate = models.DateTimeField()
    status = models.CharField(
        _('status'), default=ReservationStatus.PENDING, choices=ReservationStatus.choices(), max_length=32
    )

    def __str__(self):
        return ', '.join([bike.name for bike in self.bikes.all()]) +\
               ' [' + str(self.requestDate.strftime('%Y-%m-%d %H:%m')) + ']'

class Complaint(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    lastUpdate = models.DateTimeField(default=now)
    customer = models.ForeignKey(User, related_name='complaint', on_delete=models.CASCADE)
    description = models.CharField(max_length=256)
    status = models.CharField(
        _('status'), default=ComplaintStatus.OPENED, choices=ComplaintStatus.choices(), max_length=32
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
