from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class CustomerFeedback(models.Model):
    name = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    feedback = models.TextField()
    approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.company}) - {self.rating}★"