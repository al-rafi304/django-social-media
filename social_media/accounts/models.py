from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Account(AbstractUser):
    dob = models.DateField()
    bio = models.CharField(max_length=160)
    phone = models.CharField(max_length = 50, null=True, blank=True)
    hometown = models.CharField(max_length=100, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    occupation = models.CharField(max_length=160, null=True, blank=True)

    SINGLE = 'SN'
    MINGLE = 'IR'
    MARRIED = 'MR'
    COMPLICATED = "CM"

    RELATIONSHIP_CHOICES = [
        (SINGLE, 'Single'),
        (MINGLE, 'In a relationship'),
        (MARRIED, 'Married'),
        (COMPLICATED, "It's complicated")
    ]

    relationshipStatus = models.CharField(max_length = 2, choices = RELATIONSHIP_CHOICES, default = None, null=True)

    profile_img = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    cover_img = models.ImageField(upload_to='cover_pics/', blank=True, null=True)

    followerCount = models.IntegerField(default=0)
    followingCount = models.IntegerField(default=0) 


    def __str__(self) -> str:
        return self.username
