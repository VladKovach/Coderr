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
            # "working_hours",
            "type",
            "email",
            "created_at",
            # "working_from",
            # "working_to",
        ]

    # def working_hours(self):
    #     return f"{self.working_from}-{self.working_to}"
