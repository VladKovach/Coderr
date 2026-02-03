from rest_framework import serializers

from profiles_app.models import Profile


class ProfileDetailSerializer(serializers.ModelSerializer):
    """
    Serializer description
    """

    class Meta:
        model = Profile
        fields = ["user", "location", "tel", "description"]
