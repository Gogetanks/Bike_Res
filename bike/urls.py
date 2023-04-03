from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_request, name='home'),
    path('login/', views.login_request, name='login'),
    path('logout/', views.logout_request, name='logout'),
    path('register/', views.register_request, name='register'),
    path('profile/<username>', views.profile_request, name='profile'),
    path('edit_profile/', views.edit_profile_request, name='edit_profile'),
    path('delete_account/', views.delete_account_request, name='delete_account'),
    
    path('worker/', views.worker_main_request, name='worker'),
    path('worker/account_management', views.account_management_request, name='account_management'),

    path('about/', views.about, name='about'),
    path('bikes/', views.bikes, name='bikes'),
    path('reserve/', views.reserve, name='reserve'),
    path('payment/', views.payment, name='payment'),
    path('complaint/', views.complaint, name='bikes'),


]
