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
    path('bikes/', views.bike_list, name='bike_list'),
    path('bikes/<str:slug>/', views.bike_detail, name='bike_detail'),
    path('categories/', views.category_list, name='category_list'),
    path('categories/<int:pk>/', views.category_detail, name='category_detail'),
    path('search/', views.search, name='search'),

    path('reserve/<uuid:bike_id>', views.ReserveBikeView.as_view(), name='reserve'),
    path('payment/', views.payment, name='payment'),
    path('complaints/', views.complaints_request, name='complaints'),
    path('complaints/<uuid:complaint_id>/', views.complaint_request, name='complaint'),
    path('complaints/new/', views.new_complaint_request, name='new_complaint'),
    path('complaints/unattached/', views.unattached_complaints_request, name='unattached_complaints'),
    path('complaints/take/<uuid:complaint_id>/', views.take_complaint_request, name='take_complaint'),
]
