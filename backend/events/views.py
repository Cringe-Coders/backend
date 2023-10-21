from datetime import datetime

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


# class CreateEvent(CreateAPIView):
#     queryset = models.Event.objects.all()
#     serializer_class = serializers.EventCreateSerializer


class CreateEventAPIView(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request: Request):
        data = request.data
        title = data.get("title")
        text = data.get("text")
        manager_id = request.user.pk
        user = User.objects.get(pk=manager_id)
        city = data.get("city")
        street = data.get("street")
        house = data.get("house")
        coords = data.get("coords")

        event_time_start = data.get("event_time_start")
        event_time_start_i = datetime.strftime(event_time_start, '%y-%m-%d %H:%M')

        event_time_end = data.get("event_time_end")
        event_time_end_i = datetime.strftime(event_time_end, '%y-%m-%d %H:%M')

        # reg_time_end = data.get("reg_time_end")

        # participant = data.get("")
        tag_income = data.get("tag")
        price = int(data.get("price"))
        tag, created = models.Tag.objects.get_or_create(title=tag_income)
        event = models.Event.objects.create(
            title=title,
            text=text,
            manager_id=manager_id,
            city=city,
            street=street,
            house=house,
            coords=coords,
            event_time_start=event_time_start_i,
            event_time_end=event_time_end_i,
            # reg_time_end=reg_time_end,
            price=price,
        )
        event.save()
        event.tags.add(tag)
        event.participant.add(user)
        event.save()
        return Response({"status": "200"}, status=status.HTTP_200_OK)


class EventUpdate(APIView):
    permission_classes = (IsAuthenticated, )

    def put(self, request, *args, **kwargs):
        pk = kwargs.get("id", None)
        if not pk:
            return Response({"status": "404", "error": "Method PUT not allowed"})
        user = User.objects.get_or_none(pk=request.user.id)
        event = models.Event.objects.get(pk=pk)
        if user is not None and event.manager.pk == user.pk:
            serializer = serializers.EventUpdateSerializer(data=request.data, instance=event)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"status": "200", "post": serializer.data})
        return Response({"status": "404", "error": "error"})


class EventPreviewUpdateAPIView(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request: Request, id):
        preview = request.FILES["preview"]
        event = models.Event.objects.get(pk=id)
        if request.user.pk == event.manager.pk:
            if event.preview:
                event.preview.delete()
            event.preview = preview
            event.save()
            return Response({"status": "200"}, status=status.HTTP_200_OK)
        return Response({"status": "404"})
