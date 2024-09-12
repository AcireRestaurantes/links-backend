from rest_framework import viewsets
from Profile.models import UserProfile
from Profile.serializers import UserProfileSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class UserProfileViewSet(viewsets.ModelViewSet):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        # Permite acesso a todos os perfis para leitura (GET)
        if self.request.method in ['GET']:
            return UserProfile.objects.all()
        # Exige autenticação para operações de escrita (POST, PUT, PATCH, DELETE)
        return UserProfile.objects.filter(user=self.request.user)
