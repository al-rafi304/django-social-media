from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Account(AbstractUser):
    fName = models.CharField(max_length=50)
    lName = models.CharField(max_length=50)
    dob = models.DateField(null=True)
    bio = models.CharField(max_length=160)
    phone = models.CharField(max_length = 50, null=True)
    hometown = models.CharField(max_length=100, null=True)
    address = models.TextField(null=True)
    occupation = models.CharField(max_length=160, null=True)

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

    # profile_img = models.ImageField(upload_to='images/', blank=False)
    # cover_img = models.ImageField(upload_to='image/', null=True, blank=True)

    followerCount = models.IntegerField(default=0)
    followingCount = models.IntegerField(default=0) 


    def __str__(self) -> str:
        return self.username
