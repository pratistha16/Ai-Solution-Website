# core/admin.py
from django.contrib import admin
from django.contrib.auth import get_user_model
from import_export.admin import ImportExportModelAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import (
    CustomUser, Feedback, SiteSettings, AboutUs, Solution,
    ContactInquiry, BlogPost, Article, Event, EventRegistration,
    GalleryItem, Project, Tag, Project_tags, Newsletter, ActivityLog
)

# Get the custom user model
User = get_user_model()


# ---------------------------
# Custom User Admin
# ---------------------------
@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_active', 'date_joined')
    list_filter = ('role', 'is_active', 'is_staff', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('role', 'phone', 'profile_image')}), 
    )


# ---------------------------
# Site Settings Admin
# ---------------------------
@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ('site_name', 'contact_email', 'updated_by', 'updated_at')
    readonly_fields = ('updated_at',)
    
    def save_model(self, request, obj, form, change):
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)
    
    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        return False


# ---------------------------
# About Us Admin
# ---------------------------
@admin.register(AboutUs)
class AboutUsAdmin(admin.ModelAdmin):
    list_display = ('title', 'updated_by', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    
    def save_model(self, request, obj, form, change):
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


# ---------------------------
# Solution Admin
# ---------------------------
@admin.register(Solution)
class SolutionAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'is_featured', 'is_active', 'order', 'created_at')
    list_filter = ('category', 'is_featured', 'is_active')
    search_fields = ('title', 'description')
    list_editable = ('is_featured', 'is_active', 'order')
    ordering = ('order', 'title')
    readonly_fields = ('created_at', 'updated_at')


# ---------------------------
# Contact Inquiry Admin
# ---------------------------
@admin.register(ContactInquiry)
class ContactInquiryAdmin(ImportExportModelAdmin):
    list_display = ('name', 'email', 'company', 'country', 'is_read', 'is_responded', 'created_at')
    list_filter = ('is_read', 'is_responded', 'country', 'job_title', 'created_at')
    search_fields = ('name', 'email', 'company', 'message')
    readonly_fields = ('created_at', 'updated_at')
    list_editable = ('is_read', 'is_responded')
    ordering = ('-created_at',)


# ---------------------------
# Feedback Admin
# ---------------------------
@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('user', 'company', 'rating', 'is_approved', 'created_at')
    list_filter = ('rating', 'is_approved', 'created_at')
    search_fields = ('user__username', 'company', 'comment')
    list_editable = ('is_approved',)
    readonly_fields = ('created_at',)

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)


# ---------------------------
# Blog Post Admin
# ---------------------------
@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'status', 'is_featured', 'views_count', 'published_at')
    list_filter = ('status', 'category', 'is_featured', 'published_at')
    search_fields = ('title', 'excerpt', 'content')
    list_editable = ('status', 'is_featured')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('views_count', 'created_at', 'updated_at', 'published_at')
    ordering = ('-created_at',)

    def save_model(self, request, obj, form, change):
        if not obj.author_id:
            obj.author = request.user
        super().save_model(request, obj, form, change)


# ---------------------------
# Article Admin
# ---------------------------
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'article_type', 'author', 'is_featured', 'download_count', 'published_at')
    list_filter = ('article_type', 'is_featured', 'published_at')
    search_fields = ('title', 'content')
    list_editable = ('is_featured',)
    readonly_fields = ('download_count', 'created_at', 'updated_at')
    ordering = ('-published_at',)


# ---------------------------
# Event Admin
# ---------------------------
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'event_type', 'date', 'location', 'status', 'capacity', 'is_featured')
    list_filter = ('event_type', 'status', 'is_featured', 'date')
    search_fields = ('title', 'description', 'location')
    list_editable = ('status', 'is_featured')
    ordering = ('date', 'time')
    readonly_fields = ('created_at', 'updated_at')


# ---------------------------
# Event Registration Admin
# ---------------------------
@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'event', 'registration_date', 'is_confirmed', 'attended')
    list_filter = ('is_confirmed', 'attended', 'registration_date', 'event')
    search_fields = ('name', 'email', 'company')
    list_editable = ('is_confirmed', 'attended')
    ordering = ('-registration_date',)


# ---------------------------
# Gallery Item Admin
# ---------------------------
@admin.register(GalleryItem)
class GalleryItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'event_date', 'location', 'is_featured', 'order')
    list_filter = ('category', 'is_featured', 'event_date')
    search_fields = ('title', 'description', 'event_name', 'location')
    list_editable = ('is_featured', 'order')
    ordering = ('-event_date', 'order')
    readonly_fields = ('created_at', 'updated_at')


# ---------------------------
# Project & Tag Admin
# ---------------------------
class ProjectTagsInline(admin.TabularInline):
    model = Project_tags
    extra = 1

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'completed_on')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ProjectTagsInline]
    search_fields = ('title', 'summary', 'description')
    list_filter = ('completed_on',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Project_tags)
class ProjectTagsAdmin(admin.ModelAdmin):
    list_display = ('project', 'tag')


# ---------------------------
# Newsletter Admin
# ---------------------------
@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'is_active', 'subscribed_at')
    list_filter = ('is_active', 'subscribed_at')
    search_fields = ('email', 'name')
    list_editable = ('is_active',)
    ordering = ('-subscribed_at',)


# ---------------------------
# Activity Log Admin
# ---------------------------
@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'content_type', 'object_repr', 'timestamp', 'ip_address')
    list_filter = ('action', 'content_type', 'timestamp')
    search_fields = ('user__username', 'object_repr')
    readonly_fields = ('user', 'action', 'content_type', 'object_id', 'object_repr', 'timestamp', 'ip_address')
    ordering = ('-timestamp',)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
