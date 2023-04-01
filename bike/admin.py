from django.contrib import admin
from .models import *

admin.site.register(User)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug' : ('name',)}


@admin.register(Bike)
class BikeAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner', 'slug', 'price',
                    'in_stock']
    list_filter = ['in_stock']
    list_editable = ['price', 'in_stock']
    prepopulated_fields = {'slug' : ('name',)}
