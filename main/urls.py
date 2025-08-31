# main/urls.py
from django.urls import path
from . import views  # This imports your views.py file

urlpatterns = [
    path('', views.home, name='home'),  # This should match the function name
]