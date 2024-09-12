from django.urls import path
from Links.views import LinkViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'links', LinkViewSet, basename='link')

urlpatterns = router.urls
