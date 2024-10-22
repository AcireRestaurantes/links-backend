from django.urls import path, include
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView
)

from Profile.views import UserViewSet
from Links.views import LinkViewSet
from Users.views import register_view, update_username, user_detail, verify_refresh_token


router = DefaultRouter()
router.register(r'profiles', UserViewSet, basename='profile')
router.register(r'links', LinkViewSet, basename='link')

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('register/', register_view, name='register'),
    path('api/user/<str:username>/', user_detail, name='user_detail'),
    path('api/update-username/', update_username, name='update_username'),
    path('verify-refresh-token/', verify_refresh_token, name='verify_refresh_token'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

