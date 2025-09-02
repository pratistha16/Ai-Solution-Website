# events/forms.py
from django import forms
from django.forms import inlineformset_factory
from .models import Event, GalleryImage

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            "title",
            "start_time",
            "end_time",
            "location",
            "description",
            "featured_image",
            "featured",
            "status",
            "published_at",
        ]
        widgets = {
            "start_time": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "end_time": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "published_at": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "description": forms.Textarea(attrs={"rows": 6}),
        }

class GalleryImageForm(forms.ModelForm):
    class Meta:
        model = GalleryImage
        fields = ["image", "caption"]

GalleryImageFormSet = inlineformset_factory(
    Event,
    GalleryImage,
    form=GalleryImageForm,
    fields=["image", "caption"],
    extra=3,           # show 3 empty rows by default
    can_delete=True,   # allow deleting existing images
)
