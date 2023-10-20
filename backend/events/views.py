from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import OrderingFilter

from . import models
from . import serializers
from . import paginations
from . import filters


class EventFullViewSet(ModelViewSet):
    queryset = models.Event.objects.all()
    serializer_class = serializers.EventFullSerializer

    def get_paginated_response(self, data):
        return Response(data)


class EventCatalogAPIView(ListAPIView):
    queryset = models.Event.objects.all()
    serializer_class = serializers.EventCatalogSerializer
    pagination_class = paginations.CatalogPagination
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_class = filters.EventFilter
    ordering_fields = ("event_time_start",)
