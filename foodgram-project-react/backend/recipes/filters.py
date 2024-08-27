from django_filters import rest_framework

from .models import Recipe, Ingredient


class RecipeFilter(rest_framework.FilterSet):
    tags = rest_framework.AllValuesMultipleFilter(
        field_name='tags__slug',
    )
    author = rest_framework.AllValuesMultipleFilter(
        field_name='author__id',
    )
    is_favorited = rest_framework.BooleanFilter(
        method='get_is_favorited'
    )
    is_in_shopping_cart = rest_framework.BooleanFilter(
        method='get_is_in_shopping_cart'
    )

    class Meta:
        model = Recipe
        fields = ('tags', 'author', 'is_favorited', 'is_in_shopping_cart')

    def get_is_favorited(self, queryset, name, value):
        user = self.request.user
        if value is True:
            return queryset.filter(favorites__user=user)

    def get_is_in_shopping_cart(self, queryset, name, value):
        user = self.request.user
        if value is True:
            return queryset.filter(purchases__user=user)
        return Recipe.objects.all()

class IngredientNameFilter(rest_framework.FilterSet):
    name = rest_framework.CharFilter(field_name='name', lookup_expr='istartswith')

    class Meta:
        model = Ingredient
        fields = ('name', 'measurement_unit')
