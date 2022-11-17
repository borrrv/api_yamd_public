from django.urls import path
from .views import registraions, get_token

urlpatterns = [
    path('v1/auth/signup/', registraions, name='registrations'),
    path('v1/auth/token/', get_token, name='get_token'),
]
