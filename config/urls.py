# config/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Django's built-in admin (optional; keep if you still want it)
    path('djadmin/', admin.site.urls),

    # Your custom admin console (namespaced)
    path('admin/', include('custom_admin.urls', namespace='custom_admin')),

    # Public site apps
    path('', include('main.urls')),
    path('solutions/', include('solutions.urls')),
    path('feedback/', include('feedback.urls')),
    path('articles/', include('articles.urls')),
    path('events/', include('events.urls')),
    path('contact/', include('contact.urls')),
    path('', include('solutions.urls')), 
]

# Serve media files in development
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    # Only append if MEDIA_URL/ROOT are defined in settings
    urlpatterns += static(getattr(settings, 'MEDIA_URL', '/media/'),
                          document_root=getattr(settings, 'MEDIA_ROOT', None))
