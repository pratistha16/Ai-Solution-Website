# custom_admin/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView

# Import forms and models
from solutions.models import SoftwareSolution
from solutions.forms import SoftwareSolutionForm
from articles.models import Article
from articles.forms import ArticleForm
from blogs.models import Blog
from blogs.forms import BlogForm
from events.models import Event
from events.forms import EventForm, GalleryImageFormSet
from contact.models import Contact


# ------------------------------------------
# Helper function
def staff_required(user):
    return user.is_staff


# ------------------------------------------
# Admin Login / Logout
class AdminLoginView(LoginView):
    template_name = 'admin/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        # After successful login, go to dashboard
        return reverse('custom_admin:dashboard')


class AdminLogoutView(LogoutView):
    # After logout, go back to the custom admin login
    next_page = reverse_lazy('custom_admin:admin_login')


# ------------------------------------------
# Dashboard
@login_required
@user_passes_test(staff_required)
def dashboard(request):
    stats = {
        'solutions_count': SoftwareSolution.objects.count(),
        'articles_count': Article.objects.count(),
        'blogs_count': Blog.objects.count(),
        'events_count': Event.objects.count(),
        'contacts_count': Contact.objects.count(),
    }
    return render(request, 'admin/dashboard.html', {'stats': stats})


# ------------------------------------------
# Solutions CRUD
@login_required
@user_passes_test(staff_required)
def solution_list(request):
    solutions = SoftwareSolution.objects.all()
    return render(request, 'admin/solutions/list.html', {'solutions': solutions})


@login_required
@user_passes_test(staff_required)
def solution_detail(request, pk):
    solution = get_object_or_404(SoftwareSolution, pk=pk)
    return render(request, 'admin/solutions/detail.html', {'solution': solution})


@login_required
@user_passes_test(staff_required)
def solution_create(request):
    if request.method == 'POST':
        form = SoftwareSolutionForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save()
            messages.success(request, 'Solution created successfully.')
            return redirect('custom_admin:solution_detail', pk=obj.pk)
        messages.error(request, 'Please fix the errors below.')
    else:
        form = SoftwareSolutionForm()
    return render(request, 'admin/solutions/form.html', {'form': form})


def solution_edit(request, pk):
    solution = get_object_or_404(SoftwareSolution, pk=pk)
    if request.method == "POST":
        form = SoftwareSolutionForm(request.POST, request.FILES, instance=solution)
        if form.is_valid():
            form.save()
            messages.success(request, "Solution updated.")
            return redirect("custom_admin:solution_detail", pk=solution.pk)
        messages.error(request, "Please fix the errors below.")
    else:
        form = SoftwareSolutionForm(instance=solution)

    return render(
        request,
        "admin/solutions/form.html",
        {"form": form, "title": "Edit Solution", "solution": solution},  # <—
    )


@login_required
@user_passes_test(staff_required)
def solution_delete(request, pk):
    solution = get_object_or_404(SoftwareSolution, pk=pk)
    if request.method == 'POST':
        solution.delete()
        messages.success(request, 'Solution deleted.')
        return redirect('custom_admin:solution_list')
    return render(request, 'admin/solutions/confirm_delete.html', {'object': solution})


# ------------------------------------------
# Articles CRUD
@login_required
@user_passes_test(staff_required)
def admin_article_list(request):
    articles = Article.objects.all()
    return render(request, 'admin/articles/list.html', {'articles': articles})


@login_required
@user_passes_test(staff_required)
def admin_article_create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Article created.')
            return redirect('custom_admin:admin_article_list')
        messages.error(request, 'Please fix the errors below.')
    else:
        form = ArticleForm()
    return render(request, 'admin/articles/form.html', {'form': form, 'title': 'Add Article'})


@login_required
@user_passes_test(staff_required)
def admin_article_edit(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            messages.success(request, 'Article updated.')
            return redirect('custom_admin:admin_article_list')
        messages.error(request, 'Please fix the errors below.')
    else:
        form = ArticleForm(instance=article)
    return render(request, 'admin/articles/form.html', {'form': form, 'title': 'Edit Article'})


@login_required
@user_passes_test(staff_required)
def admin_article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    return render(request, 'admin/articles/detail.html', {'article': article})


@login_required
@user_passes_test(staff_required)
def admin_article_delete(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == 'POST':
        article.delete()
        messages.success(request, 'Article deleted.')
        return redirect('custom_admin:admin_article_list')
    return render(request, 'admin/articles/confirm_delete.html', {'object': article})


# ------------------------------------------
# Blogs CRUD
@login_required
@user_passes_test(staff_required)
def admin_blog_list(request):
    blogs = Blog.objects.all()
    return render(request, 'admin/blogs/list.html', {'blogs': blogs})


@login_required
@user_passes_test(staff_required)
def admin_blog_create(request):
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Blog created.')
            return redirect('custom_admin:admin_blog_list')
        messages.error(request, 'Please fix the errors below.')
    else:
        form = BlogForm()
    return render(request, 'admin/blogs/form.html', {'form': form, 'title': 'Add Blog'})


@login_required
@user_passes_test(staff_required)
def admin_blog_edit(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            form.save()
            messages.success(request, 'Blog updated.')
            return redirect('custom_admin:admin_blog_list')
        messages.error(request, 'Please fix the errors below.')
    else:
        form = BlogForm(instance=blog)
    return render(request, 'admin/blogs/form.html', {'form': form, 'title': 'Edit Blog'})


@login_required
@user_passes_test(staff_required)
def admin_blog_detail(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    return render(request, 'admin/blogs/detail.html', {'blog': blog})


@login_required
@user_passes_test(staff_required)
def admin_blog_delete(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    if request.method == 'POST':
        blog.delete()
        messages.success(request, 'Blog deleted.')
        return redirect('custom_admin:admin_blog_list')
    return render(request, 'admin/blogs/confirm_delete.html', {'object': blog})


# ------------------------------------------
# Events CRUD
@login_required
@user_passes_test(staff_required)
def admin_event_list(request):
    events = Event.objects.all()
    return render(request, 'admin/events/list.html', {'events': events})

@login_required
@user_passes_test(staff_required)
def admin_event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    return render(request, 'admin/events/detail.html', {'event': event})

@login_required
@user_passes_test(staff_required)
def admin_event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Event created.')
            return redirect('custom_admin:admin_event_list')
        messages.error(request, 'Please fix the errors below.')
    else:
        form = EventForm()
    return render(request, 'admin/events/form.html', {'form': form, 'title': 'Add Event'})


@login_required
@user_passes_test(staff_required)
def admin_event_create(request):
    if request.method == "POST":
        form = EventForm(request.POST, request.FILES)
        formset = GalleryImageFormSet(request.POST, request.FILES)
        if form.is_valid() and formset.is_valid():
            event = form.save()
            # bind the saved event to the formset and save images
            formset.instance = event
            formset.save()
            messages.success(request, "Event created.")
            return redirect("custom_admin:admin_event_detail", pk=event.pk)
        messages.error(request, "Please fix the errors below.")
    else:
        form = EventForm()
        formset = GalleryImageFormSet()

    return render(
        request,
        "admin/events/form.html",
        {"form": form, "formset": formset, "title": "Add Event"},
    )

@login_required
@user_passes_test(staff_required)
def admin_event_create(request):
    if request.method == "POST":
        form = EventForm(request.POST, request.FILES)
        formset = GalleryImageFormSet(request.POST, request.FILES)
        if form.is_valid() and formset.is_valid():
            event = form.save()
            # bind the saved event to the formset and save images
            formset.instance = event
            formset.save()
            messages.success(request, "Event created.")
            return redirect("custom_admin:admin_event_detail", pk=event.pk)
        messages.error(request, "Please fix the errors below.")
    else:
        form = EventForm()
        formset = GalleryImageFormSet()

    return render(
        request,
        "admin/events/form.html",
        {"form": form, "formset": formset, "title": "Add Event"},
    )

@login_required
@user_passes_test(staff_required)
def admin_event_edit(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == "POST":
        form = EventForm(request.POST, request.FILES, instance=event)
        formset = GalleryImageFormSet(request.POST, request.FILES, instance=event)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, "Event updated.")
            return redirect("custom_admin:admin_event_detail", pk=event.pk)
        messages.error(request, "Please fix the errors below.")
    else:
        form = EventForm(instance=event)
        formset = GalleryImageFormSet(instance=event)

    return render(
        request,
        "admin/events/form.html",
        {"form": form, "formset": formset, "title": "Edit Event"},
    )


@login_required
@user_passes_test(staff_required)
def admin_event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    return render(request, 'admin/events/detail.html', {'event': event})


@login_required
@user_passes_test(staff_required)
def admin_event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        event.delete()
        messages.success(request, 'Event deleted.')
        return redirect('custom_admin:admin_event_list')
    return render(request, 'admin/events/confirm_delete.html', {'object': event})
