from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_request, name='home'),
    # user's authentication & things
    path('login/', views.login_request, name='login'),
    path('logout/', views.logout_request, name='logout'),
    path('register/', views.register_request, name='register'),
    path('profile/', views.profile_request, name='profile'),
    path('edit_profile/', views.edit_profile_request, name='edit_profile'),
    path('delete_account/', views.delete_account_request, name='delete_account'),
    # worker pages
    path('worker/', views.worker_main_request, name='worker'),
    path('worker/account_management', views.account_management_request, name='account_management'),
    # worker's account management
    path('deactivate-user/<int:user_id>/', views.deactivate_user, name='deactivate_user'),
    path('delete-user/<int:user_id>/', views.delete_user, name='delete_user'),

    path('about/', views.about, name='about'),
    path('bikes/', views.bikes, name='bikes'),
    path('reserve/', views.reserve, name='reserve'),
    path('payment/', views.payment, name='payment'),
    path('complaints/', views.complaints_request, name='complaints'),
    path('complaints/<uuid:complaint_id>/', views.complaint_request, name='complaint'),
    path('complaints/new/', views.new_complaint_request, name='new_complaint'),
    path('complaints/unattached/', views.unattached_complaints_request, name='unattached_complaints'),
]
