from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_request, name='home'),
    # user's authentication & things
    path('login/', views.login_request, name='login'),
    path('logout/', views.logout_request, name='logout'),
    path('register/', views.register_request, name='register'),
    path('profile/', views.profile_request, name='profile'),
    path('topup_account/', views.topup_account_request, name='topup_account'),
    path('edit_profile/', views.edit_profile_request, name='edit_profile'),
    path('delete_account/', views.delete_account_request, name='delete_account'),

    path('mechanic/', views.mechanic_main_request, name='mechanic'),

    # worker pages
    path('worker/', views.worker_main_request, name='worker'),
    path('worker/account_management', views.account_management_request, name='account_management'),
    path('worker/invoice_management', views.invoice_management_request, name='invoice_management'),
    path('worker/invoice_management/worker_pay_invoice/<int:invoice_id>', views.worker_pay_invoice, name='worker_pay_invoice'),
    path('worker/invoice_management/cancel_invoice/<int:invoice_id>', views.cancel_invoice, name='cancel_invoice'),
    path('worker/invoice_management/delete_invoice/<int:invoice_id>', views.delete_invoice, name='delete_invoice'),
    path('worker/reservations', views.all_reservations_request, name='all_reservations'),

    # worker's account management
    path('deactivate-user/<int:user_id>/', views.deactivate_user, name='deactivate_user'),
    path('delete-user/<int:user_id>/', views.delete_user, name='delete_user'),

    # bikes
    path('about/', views.about, name='about'),
    path('bikes/', views.bike_list, name='bike_list'),
    path('bikes/<str:slug>/', views.bike_detail, name='bike_detail'),
    path('bikes/<str:slug>/status/', views.bike_status, name='bike_status'),
    path('bikes/<str:slug>/lock/', views.bike_lock, name='bike_lock'),
    path('bikes/<str:slug>/unlock/', views.bike_unlock, name='bike_unlock'),

    path('categories/', views.category_list, name='category_list'),
    path('categories/<str:slug>/', views.category_detail, name='category_detail'),
    path('search/', views.search, name='search'),
    path('bikemap/', views.bikemap, name='bikemap'),

    path('reserve/<uuid:bike_id>', views.ReserveBikeView.as_view(), name='reserve'),
    path('reservation/<uuid:pk>/summary/', views.ReservationSummaryView.as_view(), name='reservation_summary'),
    path('reservation/<uuid:reservation_id>/credit_payment/', views.make_credit_payment, name='make_credit_payment'),
    path('reservation/<uuid:reservation_id>/card_payment/', views.make_card_payment, name='make_card_payment'),
    path('reservations/', views.my_reservations_request, name='my_reservations'),
    path('reservations/<uuid:reservation_id>', views.reservation_detail, name='reservation_detail'),
    path('reservations/cancel/<uuid:reservation_id>', views.cancel_reservation_request, name='cancel_reservation'),
    path('payment/', views.payment, name='payment'),
    path('complaints/', views.complaints_request, name='complaints'),
    path('complaints/<uuid:complaint_id>/', views.complaint_request, name='complaint'),
    path('complaints/new/', views.new_complaint_request, name='new_complaint'),
    path('complaints/unattached/', views.unattached_complaints_request, name='unattached_complaints'),
    path('complaints/take/<uuid:complaint_id>/', views.take_complaint_request, name='take_complaint'),
    path('complaints/solve/<uuid:complaint_id>/', views.solve_complaint_request, name='solve_complaint'),
    path('complaints/reopen/<uuid:complaint_id>/', views.reopen_complaint_request, name='reopen_complaint'),

    # payments
    path('invoices/', views.invoices_request, name='invoices'),
    path('invoice/<int:invoice_id>', views.invoice_request, name='invoice'),

]
