# solutions/urls.py
from django.urls import path
from . import views

app_name = 'solutions'  # <- important!

urlpatterns = [
    path('', views.solution_list, name='solution_list'),               # List view
    path('<slug:slug>/', views.solution_detail, name='solution_detail') # Detail view
]
