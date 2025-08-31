from django.contrib import admin

# Register your models here.
from .models import HomePageContent

@admin.register(HomePageContent)
class HomePageContentAdmin(admin.ModelAdmin):
    list_display = ('title', 'updated_at')