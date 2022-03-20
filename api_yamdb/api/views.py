from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import Category, Genre, Title

from .permissions import IsAdminOrReadOnly
from .serializers import (CategorySerializer, GenreSerializer,
                          SignupSerializer, TitleSerializer)

User = get_user_model()


class SignupView(mixins.CreateModelMixin,
                 viewsets.GenericViewSet):
    serializer_class = SignupSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny, ]

    def create(self, request, *args, **kwargs):
        username = request.data.get('username')
        email = request.data.get('email')
        user = User.objects.filter(username=username, email=email).first()

        if not user:
            return super().create(request, *args, **kwargs)

        comfirm_token = RefreshToken.for_user(user)

        send_mail('Token comfirm',
                  f'You token comfirm is {comfirm_token}',
                  'yambd@yambd.com',
                  [user.email, ],
                  fail_silently=False)

        return Response(
            {'info': 'The confirmation key has been sent to your email'},
            status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        user = serializer.save()
        comfirm_token = RefreshToken.for_user(user)

        send_mail('Token comfirm',
                  f'You token comfirm is {comfirm_token}',
                  'yambd@yambd.com',
                  [user.email, ],
                  fail_silently=False)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class GengreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category', 'genre', 'name', 'year')
