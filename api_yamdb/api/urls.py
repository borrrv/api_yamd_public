
from django.urls import include, path
from .views import (registraions, get_token,
                    CommentViewSet, ReviewViewSet,
                    TitleViewSet, GenreViewSet,
                    UsersViewSet, CategoriesViewSet)
from rest_framework.routers import DefaultRouter

router_v1 = DefaultRouter()
router_v1.register(r'users', UsersViewSet)
router_v1.register(r'titles', TitleViewSet)
router_v1.register(r'genres', GenreViewSet)
router_v1.register(r'titles/(?P<title_id>\d+)/reviews',
                   ReviewViewSet,
                   basename='reviews')
router_v1.register(r'titles/(?P<title_id>\d+/reviews/'
                   r'(?P<review_id>)\d+/comments)',
                   CommentViewSet,
                   basename='comments')
router_v1.register(r'categories',
                   CategoriesViewSet,
                   basename='categories')


urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/signup/', registraions, name='registrations'),
    path('v1/auth/token/', get_token, name='get_token'),
]
