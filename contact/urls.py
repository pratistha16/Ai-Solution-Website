from django.urls import path
from . import views

app_name = 'contact'  # <- important

urlpatterns = [
    path('', views.contact_view, name='contact_list'),  # URL name must match template
]
