from django_filters import filters, FilterSet

from titles.models import Title


class TitleFilter(FilterSet):
    """Кастомный класс фильтров."""

    genre = filters.CharFilter(field_name='genre__slug',)
    category = filters.CharFilter(field_name='category__slug',)
    name = filters.CharFilter(field_name='name', lookup_expr='icontains',)
    year = filters.NumberFilter(field_name='year',)

    class Meta:
        model = Title
        fields = ('category', 'genre', 'name', 'year',)
