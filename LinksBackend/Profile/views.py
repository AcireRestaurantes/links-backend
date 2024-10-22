from rest_framework import serializers, viewsets
from django_filters import rest_framework as filters
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from Links.models import Link

# Serializer para o modelo Link
class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = ['url', 'text']

# Serializer para o modelo User
class UserSerializer(serializers.ModelSerializer):
    # Inclui o campo `links` como uma relação, assumindo que `Link` tem uma ForeignKey para `User` com `related_name='links'`
    links = LinkSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'date_joined',
            'is_active',
            'links'
        ]

# Filtro para o modelo User
class UserFilter(filters.FilterSet):
    username = filters.CharFilter(field_name='username', lookup_expr='iexact')

    class Meta:
        model = User
        fields = ['username']

# ViewSet para o modelo User
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()  # Utiliza o queryset padrão para User
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = UserFilter
