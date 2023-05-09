from rest_framework.routers import DefaultRouter
from api.views import TitleViewSet


router = DefaultRouter()
router.register('titles', TitleViewSet, basename='titles'),
