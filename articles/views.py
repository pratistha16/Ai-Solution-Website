from django.shortcuts import redirect, render, get_object_or_404
from .models import Article

def article_list(request):
    # Order by created_at descending (latest first)
    articles = Article.objects.all().order_by('-created_at')
    return render(request, 'articles/list.html', {'articles': articles})

def article_detail(request, slug):
    article = get_object_or_404(Article, slug=slug)
    return render(request, 'articles/detail.html', {'article': article})

