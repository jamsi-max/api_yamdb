from tkinter.messagebox import NO
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import Category, Genre, Title

from .permissions import IfUserIsAdministrator, IsAdminOrReadOnly
from .serializers import (CategorySerializer, GenreSerializer,
                          GetTokenSerializer, SignupSerializer,
                          TitleSerializer, UserSerializer)

User = get_user_model()


class SignupView(mixins.CreateModelMixin,
                 viewsets.GenericViewSet):
    serializer_class = SignupSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny, ]

    def create(self, request, *args, **kwargs):
        message = {'info': 'Код потверждения отправлен на электронную почту!'}
        headers = None
        username = request.data.get('username')
        email = request.data.get('email')
        user = User.objects.filter(username=username, email=email).first()

        if user is None:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = self.perform_create(serializer)
            message = serializer.data
            headers = self.get_success_headers(serializer.data)

        comfirm_token = RefreshToken.for_user(user)

        send_mail('Подтверждение регистрации на Yambd',
                  f'Ваш код подтверждения {comfirm_token}',
                  'yambd@yambd.com',
                  [user.email, ],
                  fail_silently=False)

        return Response(message,
                        status=status.HTTP_200_OK,
                        headers=headers)

    def perform_create(self, serializer):
        return serializer.save()


class GetTokenView(mixins.CreateModelMixin,
                   viewsets.GenericViewSet):
    permission_classes = [AllowAny, ]
    serializer_class = GetTokenSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = User.objects.filter(
            username=request.data.get('username')
        ).first()
        token = RefreshToken.for_user(user)
        access_token = str(token.access_token)

        return Response(
            {'access_token': access_token},
            status=status.HTTP_200_OK)


class UsersViewSet(viewsets.ModelViewSet):
    permission_classes = [IfUserIsAdministrator]
    pagination_class = LimitOffsetPagination
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_fields = ('username', )

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj


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
        # category = get_object_or_404(queryset, slug=request.data.get('slug'))
        # category = get_object_or_404(queryset, slug=slug)
        # category = get_object_or_404(queryset, id=pk)
        
        # category.delete()
        # return Response(status=status.HTTP_204_NO_CONTENT)


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
    filterset_fields = ('category', 'genre', 'name', 'year')
