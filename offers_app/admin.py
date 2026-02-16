from django.contrib import admin

from offers_app.models import Offer, OfferDetail

# Register your models here.


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ("user", "title", "description")
    list_filter = ("user", "title")


@admin.register(OfferDetail)
class OfferDetailAdmin(admin.ModelAdmin):
    list_display = (
        "offer",
        "delivery_time_in_days",
        "title",
        "price",
    )
    list_filter = ("offer", "price")
