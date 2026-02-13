from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.
User = get_user_model()


class Order(models.Model):
    """Model definition for Order."""

    OFFER_TYPES = (
        ("basic", "basic"),
        ("standard", "standard"),
        ("premium", "premium"),
    )

    STATUS_TYPES = (
        ("in_progress", "in_progress"),
        ("completed", "completed"),
    )

    customer_user = models.ForeignKey(
        User, related_name="customers_orders", on_delete=models.CASCADE
    )
    business_user = models.ForeignKey(
        User, related_name="business_orders", on_delete=models.CASCADE
    )
    title = models.CharField(max_length=255)
    revisions = models.IntegerField()
    delivery_time_in_days = models.IntegerField()
    price = models.IntegerField()
    features = models.JSONField(default=list, blank=True)
    offer_type = models.CharField(max_length=20, choices=OFFER_TYPES)
    status = models.CharField(
        max_length=20, choices=STATUS_TYPES, default="in_progress"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Meta definition for Order."""

        verbose_name = "Order"
        verbose_name_plural = "Orders"

    def __str__(self):
        """Unicode representation of Order."""
        return str(self.id)
