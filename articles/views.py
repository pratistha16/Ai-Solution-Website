from django.shortcuts import render

def article_list(request):
    return render(request, 'articles/list.html')

def article_detail(request, slug):
    return render(request, 'articles/detail.html', {'slug': slug})