from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse, Http404
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.utils import timezone
import json
import random
from django.urls import reverse
from django.core.paginator import Paginator
from .forms import ClientLoginForm, ContactForm, FeedbackForm, NewsletterForm, ArticleForm ,EventForm, GalleryItemForm, ClientSignupForm
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

def client_login(request):
    if request.method == "POST":
        form = ClientLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                # Redirect to feedback page after login
                return redirect('core:feedback')
            messages.error(request, "Invalid credentials")
    else:
        form = ClientLoginForm()
    return render(request, "frontend/client_login.html", {"form": form})


def client_signup(request):
    if request.method == "POST":
        form = ClientSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('core:feedback')
    else:
        form = ClientSignupForm()
    return render(request, "frontend/client_signup.html", {"form": form})

def client_logout(request):
    logout(request)
    return redirect('core:client_login')

def home(request):
    """Homepage view"""
    site_settings = SiteSettings.load() or {
        'site_name': 'Default Site Name',
        'contact_email': 'info@default.com',
        'contact_phone': '+1234567890'
    }
    
    about_us = AboutUs.objects.first() or {
        'title': 'About Us',
        'company_background': 'No company background available.',
        'mission': 'No mission statement available.',
        'vision': 'No vision statement available.',
        'values': 'No values available.'
    }

    # Get latest 3 projects
    latest_projects = Project.objects.order_by('-completed_on')[:3]

    # Get latest 3 articles
    latest_articles = Article.objects.filter(status='published').order_by('-published_at')[:3]

    # Get 3 featured solutions
    latest_solutions = Solution.objects.filter(is_active=True, is_featured=True).order_by('-created_at')[:3]

    context = {
        'settings': site_settings,
        'about_us': about_us,
        'latest_projects': latest_projects,
        'latest_articles': latest_articles,
        'latest_solutions': latest_solutions,
    }
    
    return render(request, 'frontend/index.html', context)

def about(request):
    """About us page"""
    about_us = AboutUs.objects.first()
    team_members = TeamMember.objects.filter(is_active=True)
    
    context = {
        'about_us': about_us,
        'team_members': team_members,
        'settings': SiteSettings.load(),
    }
    
    return render(request, 'frontend/about.html', context)

def solutions(request):
    """Solutions page with filtering by category and complexity"""
    
    # Get category and complexity from query parameters
    category = request.GET.get('category', '')
    # complexity = request.GET.get('complexity', '')
    
    # Start with all active solutions
    queryset = Solution.objects.filter(is_active=True)
    
    # Filter by category if provided
    if category:
        queryset = queryset.filter(category=category)
    
    # Filter by complexity if provided
    # if complexity:
    #     queryset = queryset.filter(complexity=complexity)
    
    # Order by 'order' field and 'title' field
    solutions_list = queryset.order_by('order', 'title')
    
    # Fetch categories and complexities for filters
    categories = Solution.CATEGORY_CHOICES
    # complexities = Solution.COMPLEXITY_CHOICES  # Assuming this exists in your model
    
    context = {
        'solutions': solutions_list,
        'categories': categories,
        # 'complexities': complexities,  # Pass complexities to template
        'selected_category': category,
        # 'selected_complexity': complexity,  # Pass selected complexity to template
        'settings': SiteSettings.load(),
    }
    
    return render(request, 'frontend/solutions.html', context)


def solution_detail(request, solution_slug):
    """Solution detail page"""
    # Fetch the solution using its slug
    solution = get_object_or_404(Solution, slug=solution_slug, is_active=True)
    
    # Fetch related solutions based on the category
    related_solutions = Solution.objects.filter(category=solution.category, is_active=True).exclude(id=solution.id)[:3]
    
    context = {
        'solution': solution,
        'related_solutions': related_solutions,
        'settings': SiteSettings.load(),
    }
    
    return render(request, 'frontend/solution_detail.html', context)


def contact(request):
    """Contact page with form"""
    if request.method == 'POST':
        form = ContactForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you for your message! We will get back to you soon.')
            # Use 'core:contact' if your URLs are namespaced
            return redirect('core:contact')
    else:
        form = ContactForm()
    
    context = {
        'form': form,
        'settings': SiteSettings.load(),
    }
    
    return render(request, 'frontend/contact.html', context)

# def blog(request):
#     """Blog listing page"""
#     category = request.GET.get('category', '')
#     search = request.GET.get('search', '')
    
#     queryset = BlogPost.objects.filter(status='published')
    
#     if category:
#         queryset = queryset.filter(category=category)
    
#     if search:
#         queryset = queryset.filter(
#             Q(title__icontains=search) |
#             Q(excerpt__icontains=search) |
#             Q(content__icontains=search)
#         )
    
#     paginator = Paginator(queryset, 9)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
    
#     categories = BlogPost.CATEGORY_CHOICES
    
#     context = {
#         'page_obj': page_obj,
#         'categories': categories,
#         'selected_category': category,
#         'search_query': search,
#         'settings': SiteSettings.load(),
#     }
    
#     return render(request, 'frontend/blog.html', context)

# def blog_detail(request, slug):
#     """Blog post detail page"""
#     post = get_object_or_404(BlogPost, slug=slug, status='published')
    
#     post.views_count += 1
#     post.save(update_fields=['views_count'])
    
#     related_posts = BlogPost.objects.filter(category=post.category, status='published').exclude(id=post.id)[:3]
    
#     context = {
#         'post': post,
#         'related_posts': related_posts,
#         'settings': SiteSettings.load(),
#     }
    
#     return render(request, 'frontend/blog_detail.html', context)

def articles(request):
    """Articles page"""
    article_type = request.GET.get('type', '')
    queryset = Article.objects.all()
    
    if article_type:
        queryset = queryset.filter(article_type=article_type)
    
    paginator = Paginator(queryset, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    types = Article.ARTICLE_TYPE_CHOICES  
    
    context = {
        'page_obj': page_obj,
        'types': types,
        'selected_type': article_type,
        'settings': SiteSettings.load(),
    }
    
    return render(request, 'frontend/articles.html', context)

def add_article(request):
    """Add article page"""
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('article_list')
    else:
        form = ArticleForm()
    
    return render(request, 'add_article.html', {'form': form})

def article_list(request):
    """List all articles"""
    articles = Article.objects.filter(status='published')
    return render(request, 'frontend/article_list.html', {'articles': articles})

def article_detail(request, slug):
    """Display a single article by slug"""
    article = get_object_or_404(Article, slug=slug)
    return render(request, 'frontend/article_detail.html', {'article': article})

def events(request):
    """Events page with optional add-event form"""
    
    # Handle form submission
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.created_by = request.user  # optional: track creator
            # Ensure new events default to upcoming if status is empty
            if not event.status:
                event.status = 'upcoming'
            event.save()
            messages.success(request, "Event added successfully!")
            return redirect('core:events')
    else:
        form = EventForm()

    # Filtering logic
    event_type = request.GET.get('type', '')
    status = request.GET.get('status', '')  # '' = show all

    queryset = Event.objects.all()
    if event_type:
        queryset = queryset.filter(event_type=event_type)
    if status:
        queryset = queryset.filter(status__iexact=status)

    events_list = queryset.order_by('date', 'time')

    # Pagination (9 per page)
    paginator = Paginator(events_list, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    types = Event.TYPE_CHOICES
    statuses = Event.STATUS_CHOICES

    context = {
        'events': events_list,
        'page_obj': page_obj,           # for template pagination
        'types': types,
        'statuses': statuses,
        'selected_type': event_type,
        'selected_status': status,
        'settings': SiteSettings.load(),
        'form': form,                   # for frontend add-event form
    }
    
    return render(request, 'frontend/events.html', context)


def gallery(request):
    """Gallery page with optional filtering and add-gallery form"""

    # Handle gallery item creation (optional front-end form)
    if request.method == 'POST':
        form = GalleryItemForm(request.POST, request.FILES)
        if form.is_valid():
            gallery_item = form.save(commit=False)
            gallery_item.uploaded_by = request.user
            # Optional: mark as active if you have an is_active field
            if hasattr(gallery_item, 'is_active') and gallery_item.is_active is None:
                gallery_item.is_active = True
            gallery_item.save()
            messages.success(request, "Gallery item added successfully!")
            return redirect('core:gallery')
    else:
        form = GalleryItemForm()

    category = request.GET.get('category', '')  # filter by category if given

    queryset = GalleryItem.objects.all()
    if category:
        queryset = queryset.filter(category=category)

    gallery_items = queryset.order_by('-event_date', 'order')

    categories = GalleryItem.CATEGORY_CHOICES

    # Pagination (optional, 9 per page)
    paginator = Paginator(gallery_items, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'gallery_items': gallery_items,
        'page_obj': page_obj,
        'categories': categories,
        'selected_category': category,
        'settings': SiteSettings.load(),
        'form': form,  # for frontend add-gallery form
    }

    return render(request, 'frontend/gallery.html', context)
def event_detail(request, slug):
    """Event detail page"""
    event = get_object_or_404(Event, slug=slug)
    
    event.views_count += 1
    event.save(update_fields=['views_count'])
    
    related_events = Event.objects.filter(event_type=event.event_type).exclude(id=event.id)[:3]
    
    context = {
        'event': event,
        'related_events': related_events,
        'settings': SiteSettings.load(),
    }
    
    return render(request, 'frontend/event_detail.html', context)
# AJAX Views
@require_http_methods(["POST"])
def submit_feedback(request):
    """Submit feedback via AJAX"""
    try:
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True, 'message': 'Thank you for your feedback! We appreciate your input.'})
        return JsonResponse({'success': False, 'errors': form.errors})
    except Exception:
        return JsonResponse({'success': False, 'message': 'An error occurred. Please try again.'})

@require_http_methods(["POST"])
def newsletter_signup(request):
    """Newsletter signup via AJAX"""
    try:
        form = NewsletterForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True, 'message': 'Successfully subscribed to our newsletter!'})
        return JsonResponse({'success': False, 'message': 'Please enter a valid email address.'})
    except Exception:
        return JsonResponse({'success': False, 'message': 'An error occurred. Please try again.'})

@require_http_methods(["POST"])
def chatbot_response(request):
    """Simple chatbot responses"""
    try:
        data = json.loads(request.body)
        message = data.get('message', '').lower()
        
        responses = {
            'hello': "Hello! How can I help you today?",
            'hi': "Hi there! What would you like to know about AI-Solution?",
            'services': "We offer AI solutions for Healthcare, Finance, and Education. Which area interests you?",
            'healthcare': "Our healthcare AI solutions include diagnostic assistance, patient management, and predictive analytics.",
            'finance': "Our finance AI solutions include fraud detection, risk assessment, and algorithmic trading.",
            'education': "Our education AI solutions include personalized learning, student assessment, and administrative automation.",
            'contact': "You can reach us through our contact form or email us at info@ai-solution.com",
            'pricing': "Our pricing varies based on your specific needs. Please contact us for a customized quote.",
            'demo': "We'd be happy to show you a demo! Please use our contact form to schedule one.",
            'thanks': "You're welcome! Is there anything else I can help you with?",
            'bye': "Thank you for visiting AI-Solution. Have a great day!",
        }
        
        response = "I'm sorry, I didn't understand that. Could you please rephrase your question or contact our support team?"
        
        for keyword, reply in responses.items():
            if keyword in message:
                response = reply
                break
        
        return JsonResponse({'success': True, 'response': response})
    except Exception:
        return JsonResponse({'success': False, 'response': 'Sorry, I encountered an error. Please try again.'})

def download_article(request, article_id):
    """Download article PDF"""
    article = get_object_or_404(Article, id=article_id)
    
    if article.pdf_file:
        article.download_count += 1
        article.save(update_fields=['download_count'])
        
        response = HttpResponse(article.pdf_file.read(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{article.title}.pdf"'
        return response
    else:
        raise Http404("PDF file not found")

@require_http_methods(["POST"])
def event_registration(request, event_id):
    """Event registration via AJAX"""
    try:
        event = get_object_or_404(Event, id=event_id)
        
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone', '')
        company = request.POST.get('company', '')
        
        registration, created = EventRegistration.objects.get_or_create(
            event=event,
            email=email,
            defaults={'name': name, 'phone': phone, 'company': company}
        )
        
        if created:
            return JsonResponse({'success': True, 'message': 'Successfully registered for the event!'})
        return JsonResponse({'success': False, 'message': 'You are already registered for this event.'})
    except Exception:
        return JsonResponse({'success': False, 'message': 'An error occurred. Please try again.'})
def add_event(request):
    """View for adding a new event."""
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.created_by = request.user  # Set the current user as the creator
            event.save()
            messages.success(request, 'Event added successfully.')
            return redirect('event_list')  # Redirect to the event list after successful addition
    else:
        form = EventForm()

    return render(request, 'core/add_event.html', {'form': form})
def add_gallery_item(request):
    """View for adding a new gallery item."""
    if request.method == 'POST':
        form = GalleryItemForm(request.POST, request.FILES)
        if form.is_valid():
            gallery_item = form.save(commit=False)
            gallery_item.uploaded_by = request.user  # Assuming user uploads items
            gallery_item.save()
            messages.success(request, 'Gallery item added successfully.')
            return redirect('gallery_list')  # Redirect to the gallery list after successful addition
    else:
        form = GalleryItemForm()

    return render(request, 'core/add_gallery_item.html', {'form': form})
def project_detail(request, slug):
    project = get_object_or_404(Project, slug=slug)
    return render(request, 'project_detail.html', {'project': project})
def projects(request):
    projects = Project.objects.all()  # Or filter projects as needed
    return render(request, 'projects.html', {'projects': projects})


def user_feedback(request):
    """Display feedback list and submission form for logged-in clients"""
    # Fetch all feedbacks for display
    feedback_list = Feedback.objects.all().order_by('-created_at')

    # Paginate feedbacks (5 per page)
    paginator = Paginator(feedback_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'settings': SiteSettings.load(),  # optional site settings
    }

    return render(request, 'frontend/user_feedback.html', context)
@login_required(login_url='core:client_login')
def feedback(request):
    """Feedback submission page"""
    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback_obj = form.save(commit=False)
            feedback_obj.user = request.user
            feedback_obj.save()
            messages.success(request, "Thank you for your feedback!")
            return redirect('core:feedback')
    else:
        form = FeedbackForm()
    
    return render(request, "frontend/feedback.html", {"form": form})
    


def projects(request):
    """Projects page"""
    tag = request.GET.get('tag', '')
    queryset = Project.objects.all()
    
    if tag:
        queryset = queryset.filter(tags__name__iexact=tag)
    
    paginator = Paginator(queryset, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    all_tags = Tag.objects.all()
    
    context = {
        'page_obj': page_obj,
        'all_tags': all_tags,
        'selected_tag': tag,
        'settings': SiteSettings.load(),
    }
    
    return render(request, 'frontend/projects.html', context)
def project_detail(request, slug):
    """Project detail page"""
    project = get_object_or_404(Project, slug=slug)
    
    project.views_count += 1
    project.save(update_fields=['views_count'])
    
    related_projects = Project.objects.filter(tags__in=project.tags.all()).exclude(id=project.id).distinct()[:3]
    
    context = {
        'project': project,
        'related_projects': related_projects,
        'settings': SiteSettings.load(),
    }
    
    return render(request, 'frontend/project_detail.html', context)
def password_reset_request(request):
    """Handle password reset requests"""
    if request.method == 'POST':
        email = request.POST.get('email')
        associated_users = User.objects.filter(Q(email=email))
        if associated_users.exists():
            for user in associated_users:
                subject = "Password Reset Requested"
                email_template_name = "registration/password_reset_email.txt"
                c = {
                    "email": user.email,
                    'domain': request.META['HTTP_HOST'],
                    'site_name': 'Your Site',
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "user": user,
                    'token': default_token_generator.make_token(user),
                    'protocol': 'http',
                }
                email = render_to_string(email_template_name, c)
                try:
                    send_mail(subject, email, settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=False)
                except Exception as e:
                    return JsonResponse({'success': False, 'message': f'Error sending email: {str(e)}'})
            return JsonResponse({'success': True, 'message': 'A password reset link has been sent to your email.'})
        else:
            return JsonResponse({'success': False, 'message': 'No user is associated with this email address.'})
    return render(request, 'registration/password_reset_form.html')