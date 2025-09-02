# main/urls.py
from django.urls import path
from . import views

app_name = "main"

urlpatterns = [
    path("", views.home, name="home"),
    # add other main-only routes here, e.g. "about/", "services/", etc.
]
