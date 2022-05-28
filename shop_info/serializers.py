from collections import OrderedDict

from rest_framework.serializers import ModelSerializer
from django.core.exceptions import BadRequest

from shop_info.models import Shop, Street, City


class ShopSerializer(ModelSerializer):

    class Meta:
        model = Shop
        fields = ('id', 'name', 'city', 'street',
                  'house_number', 'open_time', 'close_time',)

    def to_representation(self, instance) -> OrderedDict:
        representation = super(
            ShopSerializer, self).to_representation(instance)
        representation['city'] = instance.city.name
        representation['street'] = instance.street.name
        return representation

    def validate(self, attrs):
        city_id = attrs['street'].city.id
        street_id = attrs['city'].id
        if city_id != street_id:
            raise BadRequest
        return super().validate(attrs)
