from rest_framework.serializers import ModelSerializer

from .models import City, Street


class CitySerializer(ModelSerializer):
    class Meta:
        model = City
        fields = ('name',)


class StreetSerializer(ModelSerializer):
    class Meta:
        model = Street
        fields = ('name',)
