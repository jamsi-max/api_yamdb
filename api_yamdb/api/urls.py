from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (SignupView, GetTokenView,
                    CategoryViewSet, GengreViewSet,
                    SignupView, TitleViewSet,
                    UsersViewSet)

router = DefaultRouter()
router.register('auth/signup', SignupView, basename='signup')
router.register('auth/token', GetTokenView, basename='get_token')
router.register('users', UsersViewSet, basename='users')
router.register('categories', CategoryViewSet, basename='categories')
router.register('genres', GengreViewSet, basename='genres')
router.register('titles', TitleViewSet, basename='titles')


urlpatterns = [
    path('v1/', include(router.urls)),
]
