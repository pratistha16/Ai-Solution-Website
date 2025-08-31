from django.shortcuts import render, get_object_or_404
from .models import Event, GalleryImage

def event_list(request):
    events = Event.objects.all().order_by('-date')
    return render(request, 'events/list.html', {'events': events})

def event_detail(request, slug):
    event = get_object_or_404(Event, slug=slug)
    return render(request, 'events/detail.html', {'event': event})

def gallery_view(request):
    images = GalleryImage.objects.all().order_by('-uploaded_at')
    return render(request, 'events/gallery.html', {'images': images})