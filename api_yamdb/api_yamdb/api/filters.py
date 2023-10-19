import django_filters as filters

from reviews.models import Category, Genre, Title


class TitleFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')
    year = filters.NumberFilter()
    category = filters.ModelChoiceFilter(
        field_name='category',
        queryset=Category.objects.all(),
        to_field_name='slug'
    )
    genre = filters.ModelChoiceFilter(
        field_name='genre',
        queryset=Genre.objects.all(),
        to_field_name='slug'
    )

    class Meta:
        model = Title
        fields = ['category', 'genre', 'name', 'year']
