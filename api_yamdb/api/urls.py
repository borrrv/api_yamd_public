
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from user.views import UsersViewSet, get_token, registraions

from .views import (CategoriesViewSet, CommentViewSet, GenreViewSet,
                    ReviewViewSet, TitleViewSet)

router_v1 = DefaultRouter()
router_v1.register(r'users', UsersViewSet)
router_v1.register('titles', TitleViewSet)
router_v1.register('genres', GenreViewSet)
router_v1.register(r'titles/(?P<title_id>\d+)/reviews',
                   ReviewViewSet,
                   basename='reviews')
router_v1.register(r'titles/(?P<title_id>\d+)/reviews/'
                   r'(?P<review_id>\d+)/comments',
                   CommentViewSet,
                   basename='comments')
router_v1.register('categories',
                   CategoriesViewSet,
                   basename='categories')


urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/signup/', registraions, name='registrations'),
    path('v1/auth/token/', get_token, name='get_token'),
]
