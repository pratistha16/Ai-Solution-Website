from django.db import models
from django.utils.text import slugify
from django.utils import timezone
from django.urls import reverse
import os, uuid


def solution_upload_to(instance, filename):
    base, ext = os.path.splitext(filename)
    return f"solutions/{uuid.uuid4().hex}{ext.lower()}"


class SoftwareSolution(models.Model):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        PUBLISHED = "published", "Published"

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)

    short_description = models.CharField(max_length=300, blank=True)
    description = models.TextField()

    image = models.ImageField(upload_to=solution_upload_to, blank=True, null=True)

    featured = models.BooleanField(default=False)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PUBLISHED)
    published_at = models.DateTimeField(default=timezone.now)
    demo_link = models.URLField(blank=True, null=True, help_text="Optional demo URL for this solution")

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
        return reverse("solutions:solution_detail", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title) or "solution"
            slug = base
            i = 1
            while SoftwareSolution.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                i += 1
                slug = f"{base}-{i}"
            self.slug = slug
        if self.status == self.Status.PUBLISHED and not self.published_at:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)
