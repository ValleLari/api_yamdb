from rest_framework.routers import DefaultRouter
from api.views import CategoryViewSet, GenreViewSet, TitleViewSet


router = DefaultRouter()
router.register('categories', CategoryViewSet, basename='categories'),
router.register('genres', GenreViewSet, basename='genres'),
router.register('titles', TitleViewSet, basename='titles'),
