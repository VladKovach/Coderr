from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.

User = get_user_model()


class Review(models.Model):
    """Model definition for Review."""

    RATING_CHOICES = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
    )
    business_user = models.ForeignKey(
        User, related_name="reviews", on_delete=models.CASCADE
    )
    reviewer = models.ForeignKey(
        User, related_name="is_rewiewer", on_delete=models.CASCADE
    )
    rating = models.IntegerField(choices=RATING_CHOICES)
    description = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Meta definition for Review."""

        verbose_name = "review"
        verbose_name_plural = "reviews"

    def __str__(self):
        """Unicode representation of Review."""
        return str(self.id)
