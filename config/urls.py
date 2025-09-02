# config/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Django’s default admin (optional)
    path("djadmin/", admin.site.urls),

    # Custom admin (all custom admin URLs live under /admin/)
    path("admin/", include(("custom_admin.urls", "custom_admin"), namespace="custom_admin")),

    # Public site apps (each included exactly once)
    path("", include("main.urls")),              # homepage & site pages (do NOT re-include other apps here)
    path("solutions/", include("solutions.urls")),
    path("articles/", include("articles.urls")),
    path("blogs/", include("blogs.urls")),       # add blogs public routes if you have them
    path("events/", include("events.urls")),
    path("feedback/", include("feedback.urls")),
    path("contact/", include("contact.urls")),
]

# Serve media files only in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
