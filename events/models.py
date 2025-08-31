from django.db import models
from django.urls import reverse

class Event(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=200)
    featured_image = models.ImageField(upload_to='events/', blank=True, null=True)
    registration_url = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']
        verbose_name_plural = "Events"

    def get_absolute_url(self):
        return reverse('event_detail', args=[self.slug])

    def __str__(self):
        return f"{self.title} ({self.date.strftime('%Y-%m-%d')})"

class GalleryImage(models.Model):
    event = models.ForeignKey(
        Event, 
        on_delete=models.CASCADE, 
        related_name='images'
    )
    image = models.ImageField(upload_to='events/gallery/')
    caption = models.CharField(max_length=200, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-uploaded_at']
        verbose_name_plural = "Gallery Images"

    def __str__(self):
        if self.caption:
            return f"{self.event.title} - {self.caption}"
        return f"Image for {self.event.title}"