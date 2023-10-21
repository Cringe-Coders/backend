from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework import filters


from . import models
from . import serializers
from . import paginations
from . import filters as filt
from users.models import User


class EventFullViewSet(ModelViewSet):
    queryset = models.Event.objects.all()
    serializer_class = serializers.EventFullSerializer

    def get_paginated_response(self, data):
        return Response(data)


class EventCatalogAPIView(ListAPIView):
    queryset = models.Event.objects.all()
    serializer_class = serializers.EventCatalogSerializer
    # pagination_class = paginations.CatalogPagination
    # filterset_fields = ["title", ]
    filter_backends = [filters.SearchFilter, ]
    search_fields = ["title", ]
    # filter_backends = (DjangoFilterBackend, OrderingFilter)
    # filterset_class = filters.EventFilter
    # ordering_fields = ("event_time_start",)


class CountsAPIView(APIView):
    def get(self, request: Request):
        return Response({
            "events_count": models.Event.objects.all().count(),
            "users_count": User.objects.all().count(),
        })


class RegistrationEventAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request: Request, pk):
        user = User.objects.get_or_none(pk=request.user.pk)
        if user is not None:
            event = models.Event.objects.get(pk=pk)
            event.participant.add(user)
            event.save()
            return Response({"status": "200"}, status=status.HTTP_200_OK)
        return Response({"status": "404", "error": "User not authorized"}, status=status.HTTP_404_NOT_FOUND)


class CreateEvent(CreateAPIView):
    queryset = models.Event.objects.all()
    serializer_class = serializers.EventCreateSerializer


class CreateEventAPIView(APIView):
    def post(self, request: Request):
        data = request.data
        title = data.get("")
        text = data.get("")
        manager_id = request.user.pk
        city = data.get("")
        street = data.get("")
        house = data.get("")
        coords = data.get("")

        event_time_start = data.get("event_time_start")
        event_time_end = data.get("event_time_end")
        reg_time_end = data.get("reg_time_end")

        # participant = data.get("")
        tag = data.get("tag")
