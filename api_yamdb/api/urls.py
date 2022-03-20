from django.urls import include, path
from rest_framework.routers import DefaultRouter

# from .views import AuthViewSet, TokenViewSet, UserViewSet
from .views import CategoryViewSet, GengreViewSet, SignupView

# from rest_framework_simplejwt.views import TokenObtainPairView

router = DefaultRouter()
router.register('auth/signup', SignupView, basename='signup')
router.register('categories', CategoryViewSet, basename='categories')
router.register('genres', GengreViewSet, basename='genres')
router.register('titles', GengreViewSet, basename='titles')

urlpatterns = [
    path('v1/', include(router.urls)),
    # path('v1/auth/signup/', SignupView.as_view()),
]
