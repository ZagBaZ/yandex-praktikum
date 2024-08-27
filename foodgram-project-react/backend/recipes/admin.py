from django.contrib import admin

from recipes.models import (AmountOfIngredient, Favorite, Ingredient, Recipe,
                            ShoppingList, Tag)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'is_favorited')
    search_fields = ('name', 'author')
    list_filter = ('author', 'name', 'tags')

    def is_favorited(self, obj):
        return obj.favorites.count()


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    list_filter = ('name',)


admin.site.register(Tag)
admin.site.register(Favorite)
admin.site.register(ShoppingList)
admin.site.register(AmountOfIngredient)
