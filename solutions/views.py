from django.shortcuts import render, get_object_or_404
from .models import SoftwareSolution

# solutions/views.py
def solution_list(request):
    solutions = SoftwareSolution.objects.all()
    return render(request, 'solutions/list.html', {'solutions': solutions})

def solution_detail(request, slug):
    solution = get_object_or_404(SoftwareSolution, slug=slug)
    return render(request, 'solutions/detail.html', {'solution': solution})
