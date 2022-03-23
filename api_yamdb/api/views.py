from xml.etree.ElementTree import Comment

from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import Category, Comment, Genre, Title

from .permissions import (IfUserIsAdministrator, IfUserIsAuthorOrReadOnly,
                          IsAdminOrReadOnly)
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, GetTokenSerializer,
                          ReviewSerializer, SignupSerializer, TitleSerializer,
                          UserSerializer)

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
    pagination_class = LimitOffsetPagination
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = "username"

    def get_permissions(self):
        if self.kwargs.get('username') == 'me':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IfUserIsAdministrator]
        return [permission() for permission in permission_classes]

    def retrieve(self, request, username=None):
        if username == 'me':
            username = request.user.username

        queryset = User.objects.all()
        user = get_object_or_404(queryset, username=username)
        serializer = UserSerializer(user)

        return Response(serializer.data)

    def partial_update(self, request, username=None):
        if username == 'me':
            username = request.user.username

        queryset = User.objects.all()
        user = get_object_or_404(queryset, username=username)
        serializer = UserSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        if request.user.role == 'user':
            serializer.save(role='user')
        else:
            serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, username=None):
        if request.user.role == 'admin' or request.user.is_superuser:
            super().destroy(request, username=None)
            return Response(
                {'info': 'Объект успешно удален'},
                status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(
                {'info': 'Метод не разрешен'},
                status=status.HTTP_405_METHOD_NOT_ALLOWED)

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

    search_fields = ('name', 'slug')

    # def destroy(self, request, pk=None):
    #     queryset = Category.objects.all()
    #     category = get_object_or_404(queryset, slug=self.kwargs['slug'])
    #     category = get_object_or_404(queryset, slug=request.data.get('slug'))
    #     category = get_object_or_404(queryset, slug=slug)
    #     category = get_object_or_404(queryset, id=pk)
    #     category.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)


class GengreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)

    search_fields = ('name', 'slug')


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
