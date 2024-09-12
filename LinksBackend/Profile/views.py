from rest_framework import viewsets
from Profile.models import UserProfile
from Profile.serializers import UserProfileSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticatedOrReadOnly] 

    def get_queryset(self):
        return UserProfile.objects.filter(user=self.request.user)


