from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True)
    is_approved = models.BooleanField(default=False)
    
    def __str__(self):
        return self.email
