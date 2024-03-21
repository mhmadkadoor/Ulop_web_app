from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.courses, name='courses'),
    path('sign/', views.sign, name='signup'),
    path('login/', views.login, name='login'),
]