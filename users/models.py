from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class CustomUser(AbstractUser):
    RESTAURANT = 'R'
    DELIVERY_EXECUTIVE = 'DE'

    ROLE_CHOICES = [(RESTAURANT, 'Restaurant'), (DELIVERY_EXECUTIVE, 'Delivery Executive')]

    role = models.CharField(
        choices=ROLE_CHOICES,
        max_length=2
    )

    def __str__(self):
        return self.username

