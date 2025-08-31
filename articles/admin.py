from django.contrib import admin
from .models import Article
# Register your models here.
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'is_published')
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('is_published',)
    search_fields = ('title', 'content')