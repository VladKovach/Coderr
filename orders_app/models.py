from django.db import models

# Create your models here.


class Order(models.Model):
    """Model definition for Order."""

    class Meta:
        """Meta definition for Order."""

        verbose_name = "Order"
        verbose_name_plural = "Orders"

    def __str__(self):
        """Unicode representation of Order."""
        return str(self.id)
