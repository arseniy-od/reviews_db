from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('users', views.UserViewSet)
router.register('titles', views.TitleViewSet)
router.register('categories', views.CategoryViewSet)
router.register('genres', views.GenreViewSet)
router.register('titles/(?P<title_id>[0-9]+)/reviews', views.ReviewViewSet, basename='review')
router.register('titles/(?P<title_id>[0-9]+)/reviews/(?P<review_id>[0-9]+)/comments',
                views.CommentViewSet,
                basename='comment')

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/me/', views.UpdateUser.as_view(), name='user_update'),
    path('', include(router.urls))
]
