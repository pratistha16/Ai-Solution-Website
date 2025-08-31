from django.db import models
from django.urls import reverse

class SoftwareSolution(models.Model):
    INDUSTRY_CHOICES = [
        ('healthcare', 'Healthcare'),
        ('finance', 'Finance'),
        ('retail', 'Retail'),
        ('manufacturing', 'Manufacturing'),
        ('education', 'Education'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    industry = models.CharField(max_length=100, choices=INDUSTRY_CHOICES)
    image = models.ImageField(upload_to='solutions/')
    demo_url = models.URLField(blank=True)
    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('solution_detail', args=[self.slug])

    def __str__(self):
        return self.title