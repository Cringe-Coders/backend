from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

app_name = "users"

urlpatterns = [
    path('users/registration/', SignUpView.as_view()),
    path('api/profile/', ProfileAPIView.as_view()),
    path('api/profile/update/', ProfileUpdateAPIView.as_view()),
    path('api/users/<int:pk>/', UserProfileAPIView.as_view()),
]
