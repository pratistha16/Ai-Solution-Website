from django import forms
from .models import Blog

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = [
            "title",
            "author",
            "content",
            "featured_image",
            "featured",
            "status",        # draft / published
            "published_at",
        ]
        widgets = {
            "published_at": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "content": forms.Textarea(attrs={"rows": 8}),
        }
