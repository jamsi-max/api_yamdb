from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import SignupView, GetTokenView

router = DefaultRouter()
router.register('auth/signup', SignupView, basename='signup')
router.register('auth/token', GetTokenView, basename='get_token')


urlpatterns = [
    path('v1/', include(router.urls)),
    # path('v1/auth/token/', GetTokenView.as_view(), name='get_token')
]
