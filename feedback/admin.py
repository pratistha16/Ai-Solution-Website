from django.contrib import admin
from .models import CustomerFeedback

@admin.register(CustomerFeedback)
class CustomerFeedbackAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'rating', 'approved')
    list_filter = ('approved', 'rating')
    search_fields = ('name', 'company', 'feedback')