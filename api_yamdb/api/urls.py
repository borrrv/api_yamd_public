from django.urls import path, include
from .views import registraions, get_token, TitleViewSet, GenreViewSet
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register('titles', TitleViewSet)
router.register('genres', GenreViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', registraions, name='registrations'),
    path('v1/auth/token/', get_token, name='get_token'),
]
