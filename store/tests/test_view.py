import json

from rest_framework.reverse import reverse_lazy
from rest_framework.test import APITestCase

from store.models import Product
from store.tests.factories import ProductFactory


class ProductViewTest(APITestCase):

    def setUp(self) -> None:
        self.product = ProductFactory()

    def test_list(self):
        url = reverse_lazy('store:list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200, response.data)
        self.assertEqual(len(response.data), Product.objects.all().count(), response.data)

    def test_create(self):
        url = reverse_lazy('store:list')
        data = {
            'title': 'Название',
            'cost_price': 10,
            'price': 100,
            'amount': 111,
        }
        response = self.client.post(url, data=json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 201)

        product = Product.objects.filter(pk=response.data['id']).first()    # type: Product
        self.assertEqual(response.data['title'], product.title)
        self.assertEqual(response.data['cost_price'], product.cost_price)
        self.assertEqual(response.data['price'], product.price)
        self.assertEqual(response.data['amount'], product.amount)

    def test_retrieve(self):
        url = reverse_lazy('store:manage', kwargs=dict(pk=self.product.pk))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200, response.data)
        self.assertEqual(response.data['id'], self.product.pk, response.data)

    def test_edit(self):
        url = reverse_lazy('store:manage', kwargs=dict(pk=self.product.pk))
        data = {
            'cost_price': 20,
            'price': 200,
            'amount': 222,
        }
        response = self.client.put(url, data=json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 200, response.data)
        product = Product.objects.filter(pk=response.data['id']).values('cost_price', 'price', 'amount')[0]
        for check_field in data.keys():
            self.assertEqual(product[check_field], data[check_field])

    def test_delete(self):
        url = reverse_lazy('store:manage', kwargs=dict(pk=self.product.pk))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204, response.data)
        product = Product.objects.filter(pk=self.product.pk)  # type: Product
        self.assertIsNone(product.first())
