from django.core.exceptions import BadRequest
from django.db.models import QuerySet
from rest_framework.generics import ListAPIView
from .models import City, Street
from .serializers import CitySerializer, StreetSerializer


class CityView(ListAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer


class StreetView(ListAPIView):
    serializer_class = StreetSerializer

    def get_queryset(self) -> QuerySet:
        city_id = self.kwargs['city_id']
        qs = Street.objects.filter(city=city_id)
        if qs:
            return qs
        raise BadRequest(f"There's no city with given id {city_id}")
