from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db.utils import IntegrityError
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import Category, Genre, Review, Title

from .permissions import (IfUserIsAdministrator, IfUserIsAuthorOrReadOnly,
                          IfUserIsModerator, IsAdminOrReadOnly)
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, GetTokenSerializer,
                          ReviewSerializer, SignupSerializer,
                          TitleReadSerializer, TitleSerializer, UserSerializer)

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


class CategoryViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin,
                      mixins.RetrieveModelMixin, viewsets.GenericViewSet,
                      mixins.ListModelMixin):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    lookup_field = 'slug'
    search_fields = ('name', 'slug')

    def retrieve(self, request, slug=None):
        queryset = Category.objects.all()
        try:
            category = queryset.get(slug=slug)
        except Exception:
            return Response(
                {'info': 'Метод не разрешен'},
                status=status.HTTP_405_METHOD_NOT_ALLOWED)

        serializer = CategorySerializer(category)
        return Response(serializer.data)


class GengreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'slug')
    lookup_field = 'slug'

    def retrieve(self, request, slug=None):
        queryset = Genre.objects.all()
        try:
            genre = queryset.get(slug=slug)
        except Exception:
            return Response(
                {'info': 'Метод не разрешен'},
                status=status.HTTP_405_METHOD_NOT_ALLOWED)

        serializer = GenreSerializer(genre)
        return Response(serializer.data)

    def partial_update(self, request, slug=None):
        queryset = Genre.objects.all()
        try:
            queryset.get(slug=slug)
        except Exception:
            return Response(
                {'info': 'Метод не разрешен'},
                status=status.HTTP_405_METHOD_NOT_ALLOWED)

        super.partial_update(request, slug=None)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = LimitOffsetPagination
    # !!!не работает видимо из-за разных сериалайзеов!!!
    # filter_backends = (DjangoFilterBackend,)
    # filterset_fields = ('genre__slug', 'category__slug', 'year', 'name')

    def get_queryset(self):
        queryset = Title.objects.all()

        genre = self.request.query_params.get('genre')
        category = self.request.query_params.get('category')
        year = self.request.query_params.get('year')
        name = self.request.query_params.get('name')

        if genre is not None:
            queryset = queryset.filter(genre__slug=genre)

        if category is not None:
            queryset = queryset.filter(category__slug=category)

        if year is not None:
            queryset = queryset.filter(year=year)

        if name is not None:
            queryset = queryset.filter(name__icontains=name)

        return queryset

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitleReadSerializer
        return TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend, )

    def get_permissions(self):
        if self.action in ('retrieve', 'list'):
            permission_classes = [AllowAny]
        else:
            permission_classes = [
                IfUserIsAuthorOrReadOnly
                | IfUserIsModerator
                | IfUserIsAdministrator
            ]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        title = get_object_or_404(
            Title,
            id=self.kwargs.get("title")
        )
        review_set = title.reviews.all()
        return review_set

    def perform_create(self, serializer):
        title = get_object_or_404(
            Title,
            id=self.kwargs.get("title")
        )

        serializer.save(
            author=self.request.user,
            title=title
        )

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except IntegrityError:
            return Response(
                {"info": "Повторная попытка оставить отзыв запрещена!"},
                status=status.HTTP_400_BAD_REQUEST)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)

    def get_permissions(self):
        if self.action in ('retrieve', 'list'):
            permission_classes = [AllowAny]
        else:
            permission_classes = [
                IfUserIsAuthorOrReadOnly
                | IfUserIsModerator
                | IfUserIsAdministrator
            ]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get("review_id"),
            title__id=self.kwargs["title_id"],
        )
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get("review_id"),
        )
        return serializer.save(author=self.request.user, review_id=review)
