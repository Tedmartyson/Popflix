import django_filters
from .models import House

class HouseFilter(django_filters.FilterSet):

    class Meta:
        model = House
        fields = ('address', 'price', 'area', 'floor', 'rooms')

