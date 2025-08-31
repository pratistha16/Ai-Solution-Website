from django.db import models
from django.urls import reverse

class Article(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    author = models.CharField(max_length=100)
    featured_image = models.ImageField(upload_to='articles/')
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('article_detail', args=[self.slug])

    def __str__(self):
        return self.title