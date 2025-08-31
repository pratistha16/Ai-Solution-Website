from django import forms
from .models import SoftwareSolution

class SoftwareSolutionForm(forms.ModelForm):
    class Meta:
        model = SoftwareSolution
        fields = '__all__'  # Or specify fields you want to include: ['title', 'description', 'industry', etc.]
        
        # Optional: Add widgets for better form rendering
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'industry': forms.Select(attrs={'class': 'form-control'}),
        }
        
        # Optional: Add labels
        labels = {
            'title': 'Solution Title',
            'description': 'Detailed Description',
        }