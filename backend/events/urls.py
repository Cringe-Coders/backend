from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

app_name = "events"

routers = DefaultRouter()
routers.register(r"event", EventFullViewSet)

urlpatterns = [
    path("api/", include(routers.urls)),
    path("api/events/", EventCatalogAPIView.as_view())
]
