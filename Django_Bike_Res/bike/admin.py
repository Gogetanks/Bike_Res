from django.contrib import admin
from .models import *

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    filter_horizontal = ('groups',)
    style_fields = {'groups': 'm2m_transfer'}

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug' : ('name',)}

@admin.register(Bike)
class BikeAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner', 'slug', 'price', 'in_stock']
    list_filter = ['in_stock']
    list_editable = ['price', 'in_stock']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_filter = ['status', 'requestDate', 'endDate']
    #filter_horizontal = ('bikes',)
    #style_fields = {'bikes': 'm2m_transfer'}

@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_filter = ['customer', 'status', 'lastUpdate']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_filter = ['user']

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'created_on', 'paid_on', 'due_date', 'status', 'paid_via', 'comment']
    list_filter = ['created_on', 'user', 'status']

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ['id', 'bike', 'timestamp', 'latitude', 'longitude', 'altitude', 'speed', 'track', 'climb', 'time', 'error_horizontal', 'error_vertical']
    list_filter = ['bike', 'speed', 'time']

@admin.register(BikeStatus)
class BikeStatusAdmin(admin.ModelAdmin):
    list_display = ['id', 'bike', 'time', 'is_online', 'is_locked']
    list_filter = ['bike', 'time', 'is_online', 'is_locked']
    class Meta:
        verbose_name = 'status'
        verbose_name_plural = 'status'
