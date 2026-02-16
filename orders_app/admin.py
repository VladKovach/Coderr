from django.contrib import admin

from orders_app.models import Order

# Register your models here.


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "customer_user",
        "business_user",
        "title",
        "offer_type",
        "status",
        "created_at",
    )
    list_filter = ("business_user", "title", "price")
