from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import UsersViewSet, get_token, registraions

router = DefaultRouter()

router.register(r'users', UsersViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', registraions, name='registrations'),
    path('v1/auth/token/', get_token, name='get_token'),
]
