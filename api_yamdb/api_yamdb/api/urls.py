from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

v1_router = DefaultRouter()

v1_router.register('auth/signup', views.SignUpViewSet)
v1_router.register('auth/token', views.VerifyViewSet, basename='users')
v1_router.register('users', views.UserViewSet)
v1_router.register('titles', views.TitleViewSet, basename='titles')
v1_router.register('categories', views.CategoryViewSet, basename='categories')
v1_router.register('genres', views.GenreViewSet, basename='genres')
v1_router.register(
    r'titles/(?P<title_pk>\d+)/reviews',
    views.ReviewViewSet,
    basename='reviews',
)
v1_router.register(
    r'titles/(?P<title_pk>\d+)/reviews/(?P<review_pk>\d+)/comments',
    views.CommentViewSet,
    basename='comments',
)

urlpatterns = [
    path('v1/', include(v1_router.urls)),
]
