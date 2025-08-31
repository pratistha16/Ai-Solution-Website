from django.shortcuts import render
from .models import CustomerFeedback

def feedback_list(request):
    feedbacks = CustomerFeedback.objects.filter(approved=True)
    return render(request, 'feedback/list.html', {'feedbacks': feedbacks})

def submit_feedback(request):
    # Add your feedback submission logic here
    return render(request, 'feedback/submit.html')