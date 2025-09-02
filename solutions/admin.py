from django.contrib import admin
from .models import SoftwareSolution

@admin.register(SoftwareSolution)
class SoftwareSolutionAdmin(admin.ModelAdmin):
    list_display = ("title", "status", "featured", "published_at")
    list_filter = ("status", "featured", "published_at", "created_at")
    search_fields = ("title", "short_description", "description")
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "published_at"
    ordering = ("-published_at",)
