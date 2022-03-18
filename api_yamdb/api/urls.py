from django.urls import include, path
from rest_framework.routers import DefaultRouter
# from rest_framework_simplejwt.views import TokenObtainPairView

# from .views import AuthViewSet, TokenViewSet, UserViewSet
from .views import SignupView

router = DefaultRouter()
router.register('auth/signup', SignupView, basename='signup')


urlpatterns = [
    path('v1/', include(router.urls)),
    # path('v1/auth/signup/', SignupView.as_view()),
]
