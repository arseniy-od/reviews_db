from django.shortcuts import get_object_or_404

from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.exceptions import PermissionDenied, ValidationError, MethodNotAllowed
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from django_filters.rest_framework import DjangoFilterBackend

from titles.models import User, Title, Category, Genre, Review, Comment

from .serializers import *
from .permissions import *
from .filters import *
from .mixins import *


class UpdateUser(RetrieveUpdateAPIView):
    model = User
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, AllowedUserFieldsForOwner]
    http_method_names = ['patch', 'get']

    def get_object(self):
        user = self.request.user
        self.check_object_permissions(self.request, user)
        return user


class UserViewSet(SearchMixin, UserRoleMixin, ModelViewSet):
    model = User
    queryset = User.objects.all()
    permission_classes = [IsSuperUser]
    serializer_class = UserSerializer
    lookup_field = "username"


class CategoryViewSet(SearchMixin, GetDeletedObjectsMixin, ModelViewSet):
    model = Category
    queryset = Category.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = CategorySerializer
    lookup_field = "slug"


class GenreViewSet(SearchMixin, GetDeletedObjectsMixin, ModelViewSet):
    model = Genre
    queryset = Genre.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = GenreSerializer
    lookup_field = "slug"


class TitleViewSet(ModelViewSet):
    model = Title
    queryset = Title.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = TitleSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter
    lookup_field = "id"
    ordering = ['-id']


class ReviewViewSet(ModelViewSet):
    model = Review
    permission_classes = [IsAuthorOrReadOnly, OnlyOneReviewPerUser]
    serializer_class = ReviewSerializer

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        return Review.objects.filter(title=title_id)

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(ModelViewSet):
    model = Comment
    permission_classes = [IsAuthorOrReadOnly]
    serializer_class = CommentSerializer

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        return Comment.objects.filter(review=review_id)

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        serializer.save(author=self.request.user, review=review)
