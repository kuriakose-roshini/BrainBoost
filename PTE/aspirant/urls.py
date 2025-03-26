# urls.py in your aspirant app
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_aspirant, name='aspirant_register'),
    path('login/', views.login_aspirant, name='aspirant_login'),
    path('dashboard/', views.dashboard_aspirant, name='aspirant_dashboard'),
]