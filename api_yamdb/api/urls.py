from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, CommentViewSet, GengreViewSet,
                    GetTokenView, ReviewViewSet, SignupView, TitleViewSet,
                    UsersViewSet)

router = DefaultRouter()
router.register("auth/signup", SignupView, basename="signup")
router.register("auth/token", GetTokenView, basename="get_token")
router.register("users", UsersViewSet, basename="users")
# router.register(
#     r"categories/(?P<slug>[-a-zA-Z0-9_]+)",
#     CategoryViewSet,
#     basename="categories",
# )
router.register("categories", CategoryViewSet, basename="categories")
router.register("genres", GengreViewSet, basename="genres")
router.register("titles", TitleViewSet, basename="titles")
router.register(
    r"titles/(?P<title_id>\d+)/reviews", ReviewViewSet, basename="review"
)
router.register(
    r"titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments",
    CommentViewSet,
    basename="comment",
)

urlpatterns = [
    path("v1/", include(router.urls)),
]
