from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True)
    profile_photo = models.ImageField(upload_to='profiles/', blank=True, null=True)

    def __str__(self):
        return self.user.username
