# custom_admin/urls.py
from django.urls import path
from . import views

app_name = 'custom_admin'  # ← enables namespaced URLs like custom_admin:admin_dashboard

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='admin_dashboard'),

    # Solutions (list / create / detail)
    path('solutions/', views.solution_list, name='admin_solutions'),
    path('solutions/create/', views.solution_create, name='admin_solution_create'),
    path('solutions/<int:pk>/', views.solution_detail, name='admin_solution_detail'),
    path('solutions/<int:pk>/edit/', views.solution_edit, name='admin_solution_edit'),
    path('solutions/<int:pk>/', views.solution_detail, name='admin_solution_detail'),
    # Auth
    path('login/', views.AdminLoginView.as_view(), name='admin_login'),
    path('logout/', views.AdminLogoutView.as_view(), name='admin_logout'),
]
