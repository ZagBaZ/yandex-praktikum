from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (DownloadShoppingCart, FavoriteView, IngredientViewSet,
                    RecipeViewSet, ShoppingCartView, TagViewSet)

router = DefaultRouter()
router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('tags', TagViewSet, basename='tags')
router.register('recipes', RecipeViewSet, basename='recipes')

urlpatterns = [
    path('recipes/download_shopping_cart/', DownloadShoppingCart.as_view()),
    path('recipes/<int:favorite_id>/favorite/', FavoriteView.as_view()),
    path('', include(router.urls)),
    path('recipes/<int:recipe_id>/shopping_cart/', ShoppingCartView.as_view()),
]
