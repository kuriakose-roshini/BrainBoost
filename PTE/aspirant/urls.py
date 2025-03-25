from django.urls import path
from .views import *

urlpatterns = [
    path('register/', aspirant_register, name='aspirant_register'),
    path('login/', aspirant_login, name='aspirant_login'),
    path('dashboard', aspirant_dashboard, name='aspirant_dashboard'),
]
