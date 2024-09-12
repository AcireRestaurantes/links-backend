from django.db import models
from Profile.models import UserProfile


class Link(models.Model):
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="links")
    url = models.URLField(max_length=500)
    text = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.text} - {self.url}"
