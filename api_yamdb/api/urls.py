from rest_framework.routers import DefaultRouter
from django.urls import include, path
from .views import (UserViewSet, create_user,
                    get_jwt_token)

router = DefaultRouter()
router.register('users', UserViewSet, basename='users')


auth_urlpatterns = [
    path('token/', get_jwt_token),
    path('signup/', create_user),
]

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/', include(auth_urlpatterns)),
]