import django_filters
from django_filters.rest_framework import FilterSet

from .models import Event


class EventFilter(FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Event
        fields = [
            "name"
        ]
