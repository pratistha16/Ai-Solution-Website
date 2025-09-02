from django.urls import path
from . import views

app_name = 'feedback'  # <- this is critical for namespacing

urlpatterns = [
    path('', views.feedback_list, name='feedback_list'),
]
