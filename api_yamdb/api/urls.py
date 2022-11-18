
from django.urls import include, path
from .views import (registraions, get_token,
                    CommentViewSet, ReviewViewSet,
                    TitleViewSet, GenreViewSet)
from rest_framework.routers import DefaultRouter

router_v1 = DefaultRouter()
router_v1.register('titles', TitleViewSet)
router_v1.register('genres', GenreViewSet)
router_v1.register(r'titles/(?P<title_id>\d+)/reviews',
                   ReviewViewSet,
                   basename='reviews')
router_v1.register(r'titles/(?P<title_id>\d+/reviews/'
                   r'(?P<review_id>)\d+/comments)',
                   CommentViewSet,
                   basename='comments')


urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/signup/', registraions, name='registrations'),
    path('v1/auth/token/', get_token, name='get_token'),
]
