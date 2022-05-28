from datetime import time
import json

from django.test import SimpleTestCase, TestCase
from django.urls import reverse, resolve
from rest_framework.test import APITestCase
from rest_framework import status

from .views import ShopView
from .models import Shop, Street, City
from .serializers import ShopSerializer


class TestUrl(SimpleTestCase):

    def test_shop_url_resolve(self):
        url = reverse('shop')
        self.assertEqual(resolve(url).func.view_class, ShopView)


class TestShopApi(APITestCase):

    def setUp(self):
        self.url = reverse('shop')
        self.city_1 = City.objects.create(name='Krd')
        self.city_2 = City.objects.create(name='Spb')
        self.street_1 = Street.objects.create(name='1st', city=self.city_1)
        self.street_2 = Street.objects.create(name='2st', city=self.city_1)
        self.street_3 = Street.objects.create(name='3st', city=self.city_2)
        self.shop_1 = Shop.objects.create(name='sh1', city=self.city_1,
                                          street=self.street_1, house_number=12,
                                          open_time=time(10, 0, 0), close_time=time(12, 0, 0))
        self.shop_2 = Shop.objects.create(name='sh2', city=self.city_1,
                                          street=self.street_1, house_number=32,
                                          open_time=time(9, 0, 0), close_time=time(13, 0, 0))
        self.shop_3 = Shop.objects.create(name='sh3', city=self.city_1,
                                          street=self.street_2, house_number=11,
                                          open_time=time(7, 0, 0), close_time=time(10, 0, 0))
        self.shop_4 = Shop.objects.create(name='sh4', city=self.city_2,
                                          street=self.street_3, house_number=132,
                                          open_time=time(6, 0, 0), close_time=time(23, 0, 0))
        self.shop_5 = Shop.objects.create(name='sh5', city=self.city_2,
                                          street=self.street_3, house_number=54,
                                          open_time=time(5, 0, 0), close_time=time(7, 0, 0))

    def test_get_all_shops_status_ok(self):
        response = self.client.get(self.url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_get_all_shops(self):
        response = self.client.get(self.url)
        data = ShopSerializer([self.shop_1, self.shop_2,
                               self.shop_3, self.shop_4,
                               self.shop_5], many=True).data
        self.assertEqual(data, response.data)

    def test_get_shops_by_city(self):
        response = self.client.get(reverse('shop'), {'city': self.city_1.id})
        data = ShopSerializer([self.shop_1, self.shop_2,
                               self.shop_3, ], many=True).data
        self.assertEqual(data, response.data)

    def test_get_shops_by_street(self):
        response = self.client.get(
            reverse('shop'), {'street': self.street_3.id})
        data = ShopSerializer([self.shop_4, self.shop_5], many=True).data
        self.assertEqual(data, response.data)

    def test_get_shops_by_street_and_city(self):
        response = self.client.get(reverse('shop'), {'city': self.city_2.id,
                                                     'street': self.street_3.id})
        data = ShopSerializer([self.shop_4, self.shop_5], many=True).data
        self.assertEqual(data, response.data)

    def test_get_shops_by_not_matching_city_and_street(self):
        response = self.client.get(reverse('shop'), {'city': self.city_2.id,
                                                     'street': self.street_1.id})
        data = []
        self.assertEqual(data, response.data)

    def test_get_assert_filtering_by_open_is_working(self):
        response = self.client.get(reverse('shop'), {'open': 1})
        self.assertGreaterEqual(len(response.data), 1)
        response = self.client.get(reverse('shop'), {'open': 0})
        self.assertGreaterEqual(len(response.data), 1)

    def test_post_ok(self):
        self.assertEqual(len(Shop.objects.all()), 5)
        response = self.client.post(self.url, json.dumps({'name': 'sh6', 'city': self.city_2.id,
                                                          'street': self.street_3.id, 'house_number': 54,
                                                          'open_time': time(4, 0, 0).isoformat(), 'close_time': time(9, 0, 0).isoformat()}),
                                    content_type='application/json')
        self.assertEqual(len(Shop.objects.all()), 6)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_post_unmatching_street_city(self):
        self.assertEqual(len(Shop.objects.all()), 5)
        response = self.client.post(self.url, json.dumps({'name': 'sh6', 'city': self.city_1.id,
                                                          'street': self.street_3.id, 'house_number': 54,
                                                          'open_time': time(4, 0, 0).isoformat(), 'close_time': time(9, 0, 0).isoformat()}),
                                    content_type='application/json')
        self.assertEqual(len(Shop.objects.all()), 5)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_post_city_or_street_doesnt_exist(self):
        self.assertEqual(len(Shop.objects.all()), 5)
        response = self.client.post(self.url, json.dumps({'name': 'sh6', 'city': 0,
                                                          'street': 0, 'house_number': 54,
                                                          'open_time': time(4, 0, 0).isoformat(), 'close_time': time(9, 0, 0).isoformat()}),
                                    content_type='application/json')
        self.assertEqual(len(Shop.objects.all()), 5)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_post_wrong_house(self):
        self.assertEqual(len(Shop.objects.all()), 5)
        response = self.client.post(self.url, json.dumps({'name': 'sh6', 'city': self.city_1.id,
                                                          'street': self.street_3.id, 'house_number': -1,
                                                          'open_time': time(4, 0, 0).isoformat(), 'close_time': time(9, 0, 0).isoformat()}),
                                    content_type='application/json')
        self.assertEqual(len(Shop.objects.all()), 5)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_post_wrong_time(self):
        self.assertEqual(len(Shop.objects.all()), 5)
        response = self.client.post(self.url, json.dumps({'name': 'sh6', 'city': self.city_1.id,
                                                          'street': self.street_3.id, 'house_number': 1,
                                                          'open_time': 'wrong', 'close_time': 'also wrong'}),
                                    content_type='application/json')
        self.assertEqual(len(Shop.objects.all()), 5)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_post_success_repsonse(self):
        response = self.client.post(self.url, json.dumps({'name': 'sh6', 'city': self.city_2.id,
                                                          'street': self.street_3.id, 'house_number': 54,
                                                          'open_time': time(4, 0, 0).isoformat(), 'close_time': time(9, 0, 0).isoformat()}),
                                    content_type='application/json')
        self.assertEqual(response.data, {'id': Shop.objects.last().id})


class TestShopSerializer(TestCase):

    def setUp(self):
        self.city_1 = City.objects.create(name='Krd')
        self.street_1 = Street.objects.create(name='1st', city=self.city_1)
        self.shop_1 = Shop.objects.create(name='sh1', city=self.city_1,
                                          street=self.street_1, house_number=12,
                                          open_time=time(10, 0, 0), close_time=time(12, 0, 0))

    def test_ok(self):
        data = ShopSerializer(self.shop_1).data
        expected_data = {
            'id': self.shop_1.id,
            'name': 'sh1',
            'city': self.city_1.name,
            'street': self.street_1.name,
            'house_number': 12,
            'open_time': time(10, 0, 0).isoformat(),
            'close_time': time(12, 0, 0).isoformat()
        }
        self.assertEqual(data, expected_data)
