from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
User = get_user_model()

phone_validator = RegexValidator(
    regex=r"^[0-9]{6,15}$",
    message="Phone number must contain only digits (6–15 digits).",
)
working_hours_validator = RegexValidator(
    regex=r"^(?:[0-9]|1[0-9]|2[0-3])-(?:[0-9]|1[0-9]|2[0-3])$",
    message="Use HH-HH format (0–23), e.g. 10-18",
)


class Profile(models.Model):
    """Model definition for Profile."""

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="profile",
    )
    location = models.CharField(max_length=255, blank=True, null=True)
    # tel = PhoneNumberField(region="DE", blank=True, null=True)
    tel = models.CharField(
        max_length=20, validators=[phone_validator], blank=True, null=True
    )
    description = models.TextField(blank=True, null=True)
    # working_from = models.TimeField(blank=True, null=True)
    # working_to = models.TimeField(blank=True, null=True)
    working_hours = models.CharField(
        max_length=5,  # "10-18"
        validators=[working_hours_validator],
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.working_hours:
            start, end = self.working_hours.split("-")

            if int(start) >= int(end):
                raise ValidationError(
                    {"working_hours": "Start time must be before end time."}
                )

    class Meta:
        """Meta definition for Profile."""

        verbose_name = "Profile"
        verbose_name_plural = "Profiles"

    def __str__(self):
        """Unicode representation of Profile."""
        return self.user.id
