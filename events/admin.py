from django.contrib import admin
from .models import Event, GalleryImage

class GalleryImageInline(admin.TabularInline):
    model = GalleryImage
    extra = 1
    fields = ('image', 'caption', 'uploaded_at')
    readonly_fields = ('uploaded_at',)

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'location', 'is_active', 'created_at')
    list_filter = ('is_active', 'date')
    search_fields = ('title', 'description', 'location')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [GalleryImageInline]
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'description')
        }),
        ('Event Details', {
            'fields': ('date', 'location', 'featured_image', 'registration_url')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )

@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ('event', 'caption', 'uploaded_at')
    list_filter = ('event', 'uploaded_at')
    search_fields = ('caption', 'event__title')
    readonly_fields = ('uploaded_at',)