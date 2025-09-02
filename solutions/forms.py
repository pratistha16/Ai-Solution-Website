from django import forms
from .models import SoftwareSolution

class SoftwareSolutionForm(forms.ModelForm):
    class Meta:
        model = SoftwareSolution
        fields = [
            "title",
            "short_description",
            "description",
            "image",
            "featured",
            "status",
            "published_at",
            "demo_link",   # new
        ]

        widgets = {
            "published_at": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "short_description": forms.Textarea(attrs={"rows": 3}),
            "description": forms.Textarea(attrs={"rows": 8}),
        }
