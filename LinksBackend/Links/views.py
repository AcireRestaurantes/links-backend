from rest_framework import viewsets
from Links.models import Link
from Links.serializers import LinkSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class LinkViewSet(viewsets.ModelViewSet):
    queryset = Link.objects.all()
    serializer_class = LinkSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Link.objects.filter(profile__user=self.request.user)
