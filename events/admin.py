from django.contrib import admin
from .models import Event, GalleryImage

class GalleryImageInline(admin.TabularInline):
    model = GalleryImage
    extra = 1
    readonly_fields = ("created_at",)

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "start_time", "status", "featured")
    list_filter = ("status", "featured", "start_time", "published_at", "created_at")
    search_fields = ("title", "location", "description")
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "start_time"
    ordering = ("-start_time",)
    inlines = [GalleryImageInline]

@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ("event", "caption", "created_at")
    list_filter = ("created_at", "event")
    search_fields = ("caption", "event__title")
    readonly_fields = ("created_at",)
