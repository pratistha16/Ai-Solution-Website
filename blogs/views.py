from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.utils import timezone
from .models import Blog


def blog_list(request):
    """
    Public list: only published posts whose published_at <= now.
    Supports ?q= search on title/content and paginates 9 per page.
    """
    qs = Blog.objects.filter(
        status=Blog.Status.PUBLISHED,
        published_at__lte=timezone.now(),
    )

    q = request.GET.get("q")
    if q:
        qs = qs.filter(models.Q(title__icontains=q) | models.Q(content__icontains=q))

    qs = qs.select_related().order_by("-published_at", "-created_at")

    paginator = Paginator(qs, 9)  # 9 per page; adjust to your design
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # Featured posts (top 3)
    featured = qs.filter(featured=True)[:3]

    context = {
        "page_obj": page_obj,
        "featured": featured,
        "query": q or "",
    }
    return render(request, "blogs/list.html", context)


def blog_detail(request, slug):
    """
    Public detail: fetch by slug, only if published and publish time has passed.
    """
    blog = get_object_or_404(
        Blog,
        slug=slug,
        status=Blog.Status.PUBLISHED,
        published_at__lte=timezone.now(),
    )

    # You can add "related posts" by tag/category if you add those fields later.
    context = {
        "blog": blog,
    }
    return render(request, "blogs/detail.html", context)
