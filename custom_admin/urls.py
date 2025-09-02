# custom_admin/urls.py
from django.urls import path
from . import views

app_name = "custom_admin"

# Primary, namespaced routes (recommended names)
urlpatterns = [
    # Auth
    path("login/",  views.AdminLoginView.as_view(),  name="admin_login"),
    path("logout/", views.AdminLogoutView.as_view(), name="admin_logout"),

    # Dashboard
    path("", views.dashboard, name="dashboard"),            # /admin/
    path("dashboard/", views.dashboard, name="dashboard"),  # /admin/dashboard/

    # Solutions
    path("solutions/",                   views.solution_list,   name="solution_list"),
    path("solutions/add/",               views.solution_create, name="solution_create"),
    path("solutions/<int:pk>/",          views.solution_detail, name="solution_detail"),
    path("solutions/<int:pk>/edit/",     views.solution_edit,   name="solution_edit"),
    path("solutions/<int:pk>/delete/",   views.solution_delete, name="solution_delete"),

    # Articles
    path("articles/",                    views.admin_article_list,   name="admin_article_list"),
    path("articles/add/",                views.admin_article_create, name="admin_article_create"),
    path("articles/<int:pk>/",           views.admin_article_detail, name="admin_article_detail"),
    path("articles/<int:pk>/edit/",      views.admin_article_edit,   name="admin_article_edit"),
    path("articles/<int:pk>/delete/",    views.admin_article_delete, name="admin_article_delete"),

    # Blogs
    path("blogs/",                       views.admin_blog_list,   name="admin_blog_list"),
    path("blogs/add/",                   views.admin_blog_create, name="admin_blog_create"),
    path("blogs/<int:pk>/",              views.admin_blog_detail, name="admin_blog_detail"),
    path("blogs/<int:pk>/edit/",         views.admin_blog_edit,   name="admin_blog_edit"),
    path("blogs/<int:pk>/delete/",       views.admin_blog_delete, name="admin_blog_delete"),

    # Events
    path("events/",                      views.admin_event_list,   name="admin_event_list"),
    path("events/add/",                  views.admin_event_create, name="admin_event_create"),
    path("events/<int:pk>/",             views.admin_event_detail, name="admin_event_detail"),
    path("events/<int:pk>/edit/",        views.admin_event_edit,   name="admin_event_edit"),
    path("events/<int:pk>/delete/",      views.admin_event_delete, name="admin_event_delete"),
]

# ---- Legacy aliases (optional) so old template names keep working ----
urlpatterns += [
    # dashboard
    path("", views.dashboard, name="admin_dashboard"),
    path("dashboard/", views.dashboard, name="admin_dashboard"),

    # solutions
    path("solutions/", views.solution_list, name="admin_solutions"),
    path("solutions/add/", views.solution_create, name="admin_solution_add"),
    path("solutions/<int:pk>/", views.solution_detail, name="admin_solution_detail"),
    path("solutions/<int:pk>/edit/", views.solution_edit, name="admin_solution_edit"),
    path("solutions/<int:pk>/delete/", views.solution_delete, name="admin_solution_delete"),

    # articles
    path("articles/", views.admin_article_list, name="admin_articles"),
    path("articles/add/", views.admin_article_create, name="admin_article_add"),
    path("articles/<int:pk>/", views.admin_article_detail, name="admin_article_detail"),
    path("articles/<int:pk>/edit/", views.admin_article_edit, name="admin_article_edit"),
    path("articles/<int:pk>/delete/", views.admin_article_delete, name="admin_article_delete"),

    # blogs
    path("blogs/", views.admin_blog_list, name="admin_blogs"),
    path("blogs/add/", views.admin_blog_create, name="admin_blog_add"),
    path("blogs/<int:pk>/", views.admin_blog_detail, name="admin_blog_detail"),
    path("blogs/<int:pk>/edit/", views.admin_blog_edit, name="admin_blog_edit"),
    path("blogs/<int:pk>/delete/", views.admin_blog_delete, name="admin_blog_delete"),
    path("blogs/",              views.admin_blog_list,   name="admin_blogs"),
    path("blogs/add/",          views.admin_blog_create, name="admin_blog_add"),
    path("blogs/add/",          views.admin_blog_create, name="blog_create"),
    path("blogs/add/",          views.admin_blog_create, name="admin_blogs_create"),

    # events
    path("events/", views.admin_event_list, name="admin_events"),
    path("events/add/", views.admin_event_create, name="admin_event_add"),
    path("events/<int:pk>/", views.admin_event_detail, name="admin_event_detail"),
    path("events/<int:pk>/edit/", views.admin_event_edit, name="admin_event_edit"),
    path("events/<int:pk>/delete/", views.admin_event_delete, name="admin_event_delete"),
]
