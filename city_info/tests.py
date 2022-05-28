from collections import OrderedDict

from django.test import SimpleTestCase, TestCase
from django.urls import reverse, resolve
from rest_framework.test import APITestCase
from rest_framework import status

from .views import CityView, StreetView
from .models import City, Street
from .serializers import CitySerializer, StreetSerializer


class TestUrls(SimpleTestCase):

    def test_city_url_resolve(self):
        url = reverse('city')
        self.assertEqual(resolve(url).func.view_class, CityView)

    def test_street_url_resolve(self):
        url = reverse('street', kwargs={'city_id': 1})
        self.assertEqual(resolve(url).func.view_class, StreetView)


class TestCityApi(APITestCase):

    def setUp(self):
        self.url = reverse('city')
        self.city_1 = City.objects.create(name='Krd')
        self.city_2 = City.objects.create(name='Spb')

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual([OrderedDict([('name', 'Krd')]),
                          OrderedDict([('name', 'Spb')])], response.data)

    def test_serializer_get(self):
        response = self.client.get(self.url)
        serializer_data = CitySerializer(
            [self.city_1, self.city_2], many=True).data
        self.assertEqual(serializer_data, response.data)

    def test_post(self):
        response = self.client.post(self.url)
        self.assertEqual(status.HTTP_405_METHOD_NOT_ALLOWED,
                         response.status_code)


class TestCitySerializer(TestCase):

    def setUp(self):
        self.city_1 = City.objects.create(name='Krd')
        self.city_2 = City.objects.create(name='Spb')

    def test_ok(self):
        data = CitySerializer([self.city_1, self.city_2], many=True).data
        expected_data = [
            {
                'name': 'Krd'
            },
            {
                'name': 'Spb'
            }
        ]
        self.assertEqual(expected_data, data)


class TestStreetApi(APITestCase):

    def setUp(self):
        self.city_1 = City.objects.create(name='Krd')
        self.city_2 = City.objects.create(name='Spb')
        self.street_1 = Street.objects.create(name='1st', city=self.city_1)
        self.street_2 = Street.objects.create(name='2st', city=self.city_1)
        self.street_3 = Street.objects.create(name='3st', city=self.city_2)

    def test_ok_city_1_get(self):
        url = reverse('street', kwargs={'city_id': self.city_1.id})
        response = self.client.get(url)
        data = StreetSerializer([self.street_1, self.street_2], many=True).data
        self.assertEqual(data, response.data)

    def test_ok_city_2_get(self):
        url = reverse('street', kwargs={'city_id': self.city_2.id})
        response = self.client.get(url)
        data = StreetSerializer([self.street_3], many=True).data
        self.assertEqual(data, response.data)

    def test_bad_request(self):
        url = reverse('street', kwargs={'city_id': 0})
        response = self.client.get(url)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)


class TestStreetSerializer(TestCase):

    def setUp(self):
        self.city_1 = City.objects.create(name='Krd')
        self.street_1 = Street.objects.create(name='1st', city=self.city_1)
        self.street_2 = Street.objects.create(name='2st', city=self.city_1)

    def test_ok(self):
        data = StreetSerializer([self.street_1, self.street_2], many=True).data
        expected_data = [
            {'name': '1st'},
            {'name': '2st'},
        ]
        self.assertEqual(data, expected_data)
