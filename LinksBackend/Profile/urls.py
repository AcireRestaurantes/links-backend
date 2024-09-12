from django.urls import path
from Profile.views import UserProfileViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'profiles', UserProfileViewSet, basename='profile')

urlpatterns = router.urls
