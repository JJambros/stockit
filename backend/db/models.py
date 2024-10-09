from django.db import models
from django.contrib.auth.models import User  # Importing the built-in User model

# Create your models here.

# Profile model to store additional user information
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Link Profile to User
    Fname = models.CharField(max_length=15)  # First name
    Minit = models.CharField(max_length=1, null=True, blank=True)  # Middle initial
    Lname = models.CharField(max_length=15)  # Last name
    email = models.EmailField(max_length=50, unique=True)  # Email (enforce uniqueness)
    phone_number = models.CharField(max_length=20, unique=True)  # Phone number (enforce uniqueness)

    def __str__(self):
        return f'{self.Fname} {self.Lname}'
