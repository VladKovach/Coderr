from django.contrib import admin

from reviews_app.models import Review

# Register your models here.


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "business_user",
        "reviewer",
        "rating",
        "description",
        "created_at",
    )
    list_filter = ("business_user", "reviewer", "rating")
