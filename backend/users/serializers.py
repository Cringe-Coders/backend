import datetime

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
                "title": event.title,
                "preview": {
                    "src": event.preview.url
                },
                "date": event.event_time_start.strftime('%Y-%m-%d %H:%M'),
                "city": event.city,
            })
        return result


class UserProfileUpdate(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "first_name", "last_name", "bio",
            "birthdate", "phone", "email",
        ]

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.bio = validated_data.get("bio", instance.bio)
        instance.birthdate = validated_data.get("birthdate", instance.birthdate)
        instance.phone = validated_data.get("phone", instance.phone)
        instance.email = validated_data.get("email", instance.email)
        instance.username = validated_data.get("email", instance.email)
        instance.save()
        return instance
