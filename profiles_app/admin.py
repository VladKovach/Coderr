from django.contrib import admin

from profiles_app.models import Profile

# Register your models here.


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "location",
        "tel",
        "working_hours",
        "tel",
        "created_at",
    )
    list_filter = ("user", "location", "working_hours")
