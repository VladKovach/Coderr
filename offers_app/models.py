from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.
User = get_user_model()


class Offer(models.Model):
    """Model definition for Offer."""

    user = models.ForeignKey(
        User, related_name="offers", on_delete=models.CASCADE
    )
    title = models.CharField(max_length=255, unique=True)
    image = models.ImageField(upload_to="offer/", blank=True, null=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Meta definition for Offer."""

        verbose_name = "Offer"
        verbose_name_plural = "Offers"

    def __str__(self):
        """Unicode representation of Offer."""
        return str(self.id)


class OfferDetail(models.Model):
    """Model definition for OfferDetail."""

    OFFER_TYPES = (
        ("basic", "basic"),
        ("standard", "standard"),
        ("premium", "premium"),
    )
    offer = models.ForeignKey(
        Offer, related_name="details", on_delete=models.CASCADE
    )
    title = models.CharField(max_length=255)
    revisions = models.IntegerField()
    delivery_time_in_days = models.IntegerField()
    price = models.IntegerField()
    features = models.JSONField(default=list, blank=True)
    offer_type = models.CharField(max_length=20, choices=OFFER_TYPES)

    def __str__(self):
        """Unicode representation of OfferDetail."""
        return str(self.id)
