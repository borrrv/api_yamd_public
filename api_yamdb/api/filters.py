from django_filters import rest_framework

from reviews.models import Title


class TitleFilter(rest_framework.FilterSet):
    """Фильтр для TitleViewSet."""

    name = rest_framework.CharFilter(
        field_name='name',
        lookup_expr='icontains'
    )
    category = rest_framework.CharFilter(
        field_name='category__slug',
        lookup_expr='icontains'
    )
    genre = rest_framework.CharFilter(
        field_name='genre__slug',
        lookup_expr='icontains'
    )

    class Meta:
        """Meta настройки фильтра для TitleViewSet."""

        model = Title
        fields = ['name', 'year', 'genre', 'category']
