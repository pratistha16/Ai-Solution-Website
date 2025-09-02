from django.db import models
from django.utils.text import slugify
from django.utils import timezone
from django.urls import reverse

import os, uuid


def event_upload_to(instance, filename):
    base, ext = os.path.splitext(filename)
    return f"events/{uuid.uuid4().hex}{ext.lower()}"


def event_gallery_upload_to(instance, filename):
    base, ext = os.path.splitext(filename)
    return f"events/gallery/{uuid.uuid4().hex}{ext.lower()}"


class Event(models.Model):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        PUBLISHED = "published", "Published"

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)

    start_time = models.DateTimeField(default=timezone.now)  # <-- add default
    end_time = models.DateTimeField(blank=True, null=True)

    location = models.CharField(max_length=255, blank=True)
    description = models.TextField()

    featured = models.BooleanField(default=False)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PUBLISHED)
    published_at = models.DateTimeField(default=timezone.now)

    featured_image = models.ImageField(upload_to=event_upload_to, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-start_time", "-created_at"]
        indexes = [
            models.Index(fields=["slug"]),
            models.Index(fields=["status", "published_at"]),
            models.Index(fields=["start_time"]),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("events:event_detail", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title) or "event"
            slug = base
            i = 1
            while Event.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                i += 1
                slug = f"{base}-{i}"
            self.slug = slug
        super().save(*args, **kwargs)


class GalleryImage(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="gallery_images")
    image = models.ImageField(upload_to=event_gallery_upload_to)
    caption = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Image for {self.event.title}"
