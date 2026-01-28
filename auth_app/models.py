from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class User(AbstractUser):
    USER_TYPES = (
        ("customer", "customer"),
        ("business", "business"),
    )

    type = models.CharField(max_length=20, choices=USER_TYPES)
