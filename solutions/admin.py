from django.contrib import admin
from .models import SoftwareSolution

@admin.register(SoftwareSolution)
class SoftwareSolutionAdmin(admin.ModelAdmin):
    list_display = ('title', 'industry', 'featured')
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('industry', 'featured')
    search_fields = ('title', 'description')