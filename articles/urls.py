from django.urls import path
from . import views

app_name = 'articles'  # <--- important, sets namespace

urlpatterns = [
    path('', views.article_list, name='article_list'),               # list page
    path('<slug:slug>/', views.article_detail, name='article_detail'),  # detail page
]
