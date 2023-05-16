from django_filters import FilterSet, CharFilter

from reviews.models import Title


class TitlesFilter(FilterSet):
    name = CharFilter(
        field_name='name',
        lookup_expr="icontains"
    )
    category = CharFilter(
        field_name='category__slug'
    )
    genre = CharFilter(
        field_name='genre__slug'
    )

    class Meta:
        model = Title
        fields = ['name', 'year', 'genre', 'category']