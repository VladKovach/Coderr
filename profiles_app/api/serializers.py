from datetime import datetime

from rest_framework import serializers

from profiles_app.models import Profile


class ProfileDetailSerializer(serializers.ModelSerializer):
    """
    Serializer description
    """

    username = serializers.CharField(source="user.username", read_only=True)
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    email = serializers.EmailField(source="user.email")
    type = serializers.CharField(source="user.type", read_only=True)

    class Meta:
        model = Profile
        fields = [
            "user",
            "username",
            "first_name",
            "last_name",
            # 'file',
            "location",
            "tel",
            "description",
            "working_hours",
            "type",
            "email",
            "created_at",
            # "working_from",
            # "working_to",
        ]

    # def get_working_hours(self, obj):
    #     if obj.working_from and obj.working_to:
    #         return f"{obj.working_from.hour}-{obj.working_to.hour}"
    #     return None

    def validate(self, attrs):
        # self.instance is always the existing Profile
        self.instance.full_clean()
        return attrs

    def update(self, instance, validated_data):
        user_data = validated_data.pop("user", {})

        # Update User fields
        for attr, value in user_data.items():
            setattr(instance.user, attr, value)
        instance.user.save()

        # Update Profile fields
        return super().update(instance, validated_data)
