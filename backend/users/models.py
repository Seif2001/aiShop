from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # Add any custom fields here (optional)
    # e.g., phone = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return self.username  # or self.email if you're using that as username
