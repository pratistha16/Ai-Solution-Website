from django import forms
from .models import Article

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = [
            "title",
            "author",
            "summary",
            "content",
            "featured_image",
            "featured",
            "status",        # draft / published
            "published_at",  # optional; auto-filled if blank on publish
        ]
        widgets = {
            "published_at": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "summary": forms.Textarea(attrs={"rows": 3}),
            "content": forms.Textarea(attrs={"rows": 8}),
        }

    def clean(self):
        cleaned = super().clean()
        # If status is published and no published_at provided, let model set it.
        return cleaned
