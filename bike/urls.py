from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_request, name='home'),
    path('login/', views.login_request, name='login'),
    path('logout/', views.logout_request, name='logout'),
    path('register/', views.register_request, name='register'),
    path('<username>', views.profile_request, name='profile'),
    path('about/', views.about, name='about'),
    path('bikes/', views.bikes, name='bikes'),
]
