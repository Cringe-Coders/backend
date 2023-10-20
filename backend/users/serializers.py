from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from .models import User
from events.models import Event


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id", "first_name", "last_name", "avatar", "bio",
            "birthdate", "phone", "email", "events",
        ]

    avatar = SerializerMethodField(source="get_avatar")
    events = SerializerMethodField(source="get_events")

    def get_avatar(self, obj: User):
        # user = obj.objects.get(pk=obj.pk)
        return obj.avatar.url

    def get_events(self, obj: User):
        # user = obj.objects.get(pk=obj.pk)
        result = []
        user_events = Event.objects.filter(participant=obj)
        for event in user_events:
            result.append({
                "id": event.pk,
                "preview": {
                    "src": event.preview.url
                },
                "date": event.event_time_start,
                "city": event.city,
            })
        return result
