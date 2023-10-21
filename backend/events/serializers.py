import datetime

from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from datetime import datetime, timezone

from .models import *


class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = [
            "id", "title"
        ]


class EventFullSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
            "id", "title", "text", "preview", "manager", "city", "street", "house",
            "coords", "event_time_start", "event_time_end",
            "reg_time_end", "time_until_reg_end", "participant_count", "tags",
            "time_until_reg_end",
        ]

    tags = TagsSerializer(many=True, read_only=True)
    preview = SerializerMethodField(source="get_preview")
    participant_count = serializers.IntegerField(source="get_participant_count")
    time_until_reg_end = SerializerMethodField(source="get_time_until_reg_end")
    manager = SerializerMethodField(source="get_manager")
    event_time_start = SerializerMethodField(source="event_time_start")
    event_time_end = SerializerMethodField(source="event_time_end")
    reg_time_end = SerializerMethodField(source="reg_time_end")

    def get_event_time_start(self, obj: Event):
        event_time_start = Event.objects.get(pk=obj.pk).event_time_start
        return event_time_start.strftime('%Y %m %d %H %M %S')

    def get_event_time_end(self, obj: Event):
        event_time_end = Event.objects.get(pk=obj.pk).event_time_end
        return event_time_end.strftime('%Y %m %d %H %M %S')

    def get_reg_time_end(self, obj: Event):
        reg_time_end = Event.objects.get(pk=obj.pk).reg_time_end
        return reg_time_end.strftime('%Y %m %d %H %M %S')

    def get_preview(self, obj: Event):
        event = Event.objects.get(pk=obj.pk)
        result = {
            "src": event.preview.url,
        }
        return result

    def get_time_until_reg_end(self, obj: Event):
        reg_time_end = Event.objects.get(pk=obj.pk).reg_time_end
        now = datetime.now(timezone.utc)
        delta = reg_time_end - now
        return delta.days

    def get_manager(self, obj: Event):
        manager = Event.objects.get(pk=obj.pk).manager
        try:
            avatar = manager.avatar.url
        except Exception:
            avatar = ""
        return {
            "id": manager.pk,
            "first_name": manager.first_name,
            "last_name": manager.last_name,
            "mail": manager.email,
            "avatar": avatar,
            "phone": manager.phone,
        }


class EventCatalogSerializer(serializers.ModelSerializer):
    class Meta:
       model = Event
       fields = [
           "id", "title", "participant_count", "city", "event_time_start", "event_time_end",
           "preview",
       ]

    participant_count = serializers.IntegerField(source="get_participant_count")
    preview = SerializerMethodField(source="get_preview")
    event_time_start = SerializerMethodField(source="event_time_start")
    event_time_end = SerializerMethodField(source="event_time_end")

    def get_event_time_start(self, obj: Event):
        event_time_start = Event.objects.get(pk=obj.pk).event_time_start
        return event_time_start.strftime('%Y %m %d %H %M %S')

    def get_event_time_end(self, obj: Event):
        event_time_end = Event.objects.get(pk=obj.pk).event_time_end
        return event_time_end.strftime('%Y %m %d %H %M %S')

    def get_preview(self, obj: Event):
        event = Event.objects.get(pk=obj.pk)
        result = {
            "src": event.preview.url,
        }
        return result


class EventCreateSerializer(serializers.ModelSerializer):
    class Meta:
       model = Event
       fields = [
           "title", "text", "city", "event_time_start", "event_time_end",
           "street", "house", "coords", "reg_time_end", "tags", "manager"
       ]

    tags = TagsSerializer(many=True, read_only=True)
