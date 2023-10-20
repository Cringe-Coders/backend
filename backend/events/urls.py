from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

app_name = "events"

urlpatterns = [
    path('', BaseView.as_view()),
]
