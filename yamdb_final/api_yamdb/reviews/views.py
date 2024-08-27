from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from .models import Review
from titles.models import Title

from .serializers import ReviewsSerializer, CommentsSerializer
from api.v1.permissions import IsAuthorOrAdminOrModeratorOrReadOnly


class ReviewsViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthorOrAdminOrModeratorOrReadOnly, ]
    serializer_class = ReviewsSerializer

    def _get_title(self):
        return get_object_or_404(Title,
                                 id=self.kwargs.get('title_id')
                                 )

    def get_queryset(self):
        title = self._get_title()
        return title.reviews.all()

    def perform_create(self, serializer):
        title = self._get_title()
        serializer.save(author=self.request.user, title=title)


class CommentsViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthorOrAdminOrModeratorOrReadOnly, ]
    serializer_class = CommentsSerializer

    def _get_review(self):
        return get_object_or_404(Review,
                                 title=self.kwargs.get('title_id'),
                                 id=self.kwargs.get('review_id')
                                 )

    def get_queryset(self):
        review = self._get_review()
        return review.comments.all()

    def perform_create(self, serializer):
        review = self._get_review()
        serializer.save(author=self.request.user, review=review)
