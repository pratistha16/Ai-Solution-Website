# custom_admin/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.urls import reverse, reverse_lazy

from django.contrib.auth.views import LoginView, LogoutView

from solutions.models import SoftwareSolution
from solutions.forms import SoftwareSolutionForm  # solutions/forms.py (plural)
from articles.models import Article
from events.models import Event
from contact.models import Contact


def staff_required(user):
    return user.is_staff


class AdminLoginView(LoginView):
    template_name = 'admin/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        # With app_name = 'custom_admin', we must namespace our reverse
        return reverse('custom_admin:admin_dashboard')


class AdminLogoutView(LogoutView):
    # Send users back to the custom admin login after logging out
    next_page = reverse_lazy('custom_admin:admin_login')


@login_required
@user_passes_test(staff_required)
def dashboard(request):
    stats = {
        'solutions_count': SoftwareSolution.objects.count(),
        'articles_count': Article.objects.count(),
        'events_count': Event.objects.count(),
        'contacts_count': Contact.objects.count(),
    }
    return render(request, 'admin/dashboard.html', {'stats': stats})


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
            return redirect('custom_admin:admin_solution_detail', pk=obj.pk)
        messages.error(request, 'Please fix the errors below.')
    else:
        form = SoftwareSolutionForm()
    return render(request, 'admin/solutions/form.html', {'form': form})
def solution_detail(request, pk):
    # Get the solution object or return 404 if not found
    solution = get_object_or_404(SoftwareSolution, pk=pk)
    return render(request, 'admin/solutions/detail.html', {'solution': solution})
def solution_edit(request, pk):
    solution = get_object_or_404(SoftwareSolution, pk=pk)
    if request.method == "POST":
        form = SoftwareSolutionForm(request.POST, request.FILES, instance=solution)
        if form.is_valid():
            form.save()
            return redirect('admin_solutions')
    else:
        form = SoftwareSolutionForm(instance=solution)
    return render(request, 'admin/solutions/form.html', {'form': form})