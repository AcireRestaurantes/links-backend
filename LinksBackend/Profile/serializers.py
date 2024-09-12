from rest_framework import serializers
from .models import UserProfile
from Links.serializers import LinkSerializer

class UserProfileSerializer(serializers.ModelSerializer):
    links = LinkSerializer(many=True, read_only=True)

    class Meta:
        model = UserProfile
        fields = ['name', 'username', 'image_url', 'is_free_user', 'theme', 'links']