from django.db import models

# Create your models here.
class HomePageContent(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Home Page Content"