from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet

from .serializers import CommentSerializer, ReviewSerializer
from reviews.models import Review, Title 


class TitleViewSet(ModelViewSet):
    pass


class CategoryViewSet(ModelViewSet):
    pass


class GenreViewSet(ModelViewSet):
    pass


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = ()

    def get_queryset(self):
        title = get_object_or_404(
            model=Title,
            id=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(
            model=Title,
            id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = ()

    def get_queryset(self):
        review = get_object_or_404(
            model=Review,
            id=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(
            model=Review,
            id=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)
