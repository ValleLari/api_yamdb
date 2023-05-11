from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.pagination import LimitOffsetPagination

from api.filters import TitleFilter
from api.mixins import MixinViewSet
from api.permissions import IsAdminOrReadOnly
from api.serializers import (CategorySerializer, GenreSerializer,
                             TitleViewSerializer, TitleWriteSerializer)
from reviews.models import Category, Genre, Title


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет произведений."""
    queryset = Title.objects.all()
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH'):
            return TitleWriteSerializer
        return TitleViewSerializer


class GenreViewSet(MixinViewSet):
    """Вьюсет жанров."""
    queryset = Genre.objects.all()
    pagination_class = LimitOffsetPagination
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    permission_classes = (IsAdminOrReadOnly,)
    search_fields = ('name',)
    lookup_field = 'slug'


class CategoryViewSet(MixinViewSet):
    """Вьюсет категорий."""
    queryset = Category.objects.all()
    pagination_class = LimitOffsetPagination
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    permission_classes = (IsAdminOrReadOnly,)
    search_fields = ('name',)
    lookup_field = 'slug'
