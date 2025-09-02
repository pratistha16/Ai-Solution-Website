from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.urls import reverse
import os, uuid


def blog_upload_to(instance, filename):
    base, ext = os.path.splitext(filename)
    return f"blogs/{uuid.uuid4().hex}{ext.lower()}"


class Blog(models.Model):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        PUBLISHED = "published", "Published"

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    author = models.CharField(max_length=100)
    content = models.TextField()

    featured = models.BooleanField(default=False)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PUBLISHED)
    published_at = models.DateTimeField(default=timezone.now)

    featured_image = models.ImageField(upload_to=blog_upload_to, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-published_at", "-created_at"]
        indexes = [
            models.Index(fields=["slug"]),
            models.Index(fields=["status", "published_at"]),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blogs:blog_detail", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title) or "post"
            slug = base
            i = 1
            while Blog.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                i += 1
                slug = f"{base}-{i}"
            self.slug = slug
        if self.status == self.Status.PUBLISHED and not self.published_at:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)
