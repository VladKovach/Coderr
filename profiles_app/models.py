from django.contrib.auth import get_user_model
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
User = get_user_model()


class Profile(models.Model):
    """Model definition for Profile."""

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="profile",
    )
    location = models.CharField(max_length=255, blank=True, null=True)
    tel = PhoneNumberField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    working_from = models.TimeField(blank=True, null=True)
    working_to = models.TimeField(blank=True, null=True)

    class Meta:
        """Meta definition for Profile."""

        verbose_name = "Profile"
        verbose_name_plural = "Profiles"

    def __str__(self):
        """Unicode representation of Profile."""
        pass
