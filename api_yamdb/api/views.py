from xml.etree.ElementTree import Comment
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import Category, Genre, Title, Review, Comment

from .permissions import (
    IfUserIsModerator,
    IsAdminOrReadOnly,
    IfUserIsAdministrator,
    IfUserIsAuthorOrReadOnly,
)
from .serializers import (
    GetTokenSerializer,
    SignupSerializer,
    CategorySerializer,
    GenreSerializer,
    SignupSerializer,
    TitleSerializer,
    UserSerializer,
    FullAccountSerializer,
    ReviewSerializer,
    CommentSerializer,
)


User = get_user_model()


class SignupView(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = SignupSerializer
    queryset = User.objects.all()
    permission_classes = [
        AllowAny,
    ]

    def create(self, request, *args, **kwargs):
        message = {"info": "Код потверждения отправлен на электронную почту!"}
        headers = None
        username = request.data.get("username")
        email = request.data.get("email")
        user = User.objects.filter(username=username, email=email).first()

        if user is None:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = self.perform_create(serializer)
            message = serializer.data
            headers = self.get_success_headers(serializer.data)

        comfirm_token = RefreshToken.for_user(user)

        send_mail(
            "Подтверждение регистрации на Yambd",
            f"Ваш код подтверждения {comfirm_token}",
            "yambd@yambd.com",
            [
                user.email,
            ],
            fail_silently=False,
        )

        return Response(message, status=status.HTTP_200_OK, headers=headers)

    def perform_create(self, serializer):
        return serializer.save()


class GetTokenView(mixins.CreateModelMixin, viewsets.GenericViewSet):
    permission_classes = [
        AllowAny,
    ]
    serializer_class = GetTokenSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = User.objects.filter(
            username=request.data.get("username")
        ).first()
        token = RefreshToken.for_user(user)
        access_token = str(token.access_token)

        return Response(
            {"access_token": access_token}, status=status.HTTP_200_OK
        )


class UsersViewSet(viewsets.ModelViewSet):
    permission_classes = [IfUserIsAdministrator]
    pagination_class = LimitOffsetPagination
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "username"

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, username=self.kwargs.get("username"))
        self.check_object_permissions(self.request, obj)
        return obj


# class UsersMeViewSet(mixins.ListModelMixin,
#                      mixins.UpdateModelMixin,
#                      viewsets.GenericViewSet):
#     queryset = None
# permission_classes = [IfUserIsAuthorOrReadOnly]
# serializer_class = UserSerializer

# def get_serializer_class(self):
#     if self.request.user.is_staff:
#         return FullAccountSerializer
#     return UserSerializer

# def get_object(self):
#     obj = get_object_or_404(
#         User,
#         id=self.request.user.id
#     )
#     return obj

# def list(self, request):
#     pass

# def update(self, request, pk=None):
#     pass


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)


class GengreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("category", "genre", "name", "year")


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [
        IfUserIsAuthorOrReadOnly,
    ]
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get("title_id"))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get("title_id"))
        return serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [
        IfUserIsAuthorOrReadOnly,
    ]
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)

    def get_queryset(self):
        review = get_object_or_404(
            Comment,
            id=self.kwargs.get("review_id"),
            title__id=self.kwargs["title_id"],
        )
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(
            Comment,
            id=self.kwargs.get("review_id"),
            title__id=self.kwargs["title_id"],
        )
        return serializer.save(author=self.request.user, review=review)
