from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='images/profile', blank=True, null=True)
    fathers_name = models.CharField(max_length=50)
    mellicode = models.CharField(max_length=10)

    def __str__(self):
        return self.user.username
