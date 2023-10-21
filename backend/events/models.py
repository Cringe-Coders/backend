from django.db import models

from users.models import User


class Tag(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.title}"


class Event(models.Model):
    title = models.CharField(max_length=150, default="Event", null=False)
    text = models.TextField(default="")
    preview = models.ImageField(blank=True, upload_to="events_preview", default="events_preview/no_preview.jpg")
    manager = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    city = models.CharField(max_length=30, null=True)
    street = models.CharField(max_length=100, null=True)
    house = models.CharField(max_length=100, null=True)
    coords = models.CharField(max_length=100, blank=True)
    event_time_start = models.DateTimeField()
    event_time_end = models.DateTimeField(null=True)
    reg_time_end = models.DateTimeField(null=True)
    participant = models.ManyToManyField(User, related_name="events", blank=True)
    tags = models.ManyToManyField(Tag, related_name="events", blank=True)

    def __str__(self):
        return f"{self.title}"

    def get_participant_count(self):
        return self.participant.count()
