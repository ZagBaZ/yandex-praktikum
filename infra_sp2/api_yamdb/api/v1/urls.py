from django.urls import include, path
from rest_framework import routers

from .views import (
    UserViewSet,
)

from .views import (
    CategoryViewSet,
    GenreViewSet,
    TitleViewSet
)
from reviews.views import (
    ReviewsViewSet,
    CommentsViewSet
)

app_name = 'api.v1'

router = routers.DefaultRouter()

router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewsViewSet,
    basename='reviews'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentsViewSet,
    basename='comments'
)
router.register('users', UserViewSet)

router.register(
    'titles',
    TitleViewSet,
    basename='titles'
)
router.register(
    'categories',
    CategoryViewSet,
    basename='categories'
)
router.register(
    'genres',
    GenreViewSet,
    basename='genres'
)


urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls.jwt')),
    path('auth/', include('users.urls')),
]
