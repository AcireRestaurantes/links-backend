from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=False)
    username = models.SlugField(unique=True)
    image_url = models.URLField(default='/profiles/profile.jpg')
    is_free_user = models.BooleanField(default=True)
    theme = models.CharField(max_length=100, default='theme-default')

    def __str__(self):
        return self.username
