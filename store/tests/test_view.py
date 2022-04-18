import json

from rest_framework.reverse import reverse_lazy
from rest_framework.test import APITestCase

from store.choices import Status
from store.models import Product, Order
from store.tests.factories import ProductFactory, OrderFactory


class ProductViewTest(APITestCase):

    def setUp(self) -> None:
        self.product = ProductFactory()

    def test_list(self):
        url = reverse_lazy('store:product_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200, response.data)
        self.assertEqual(len(response.data), Product.objects.all().count(), response.data)

    def test_create(self):
        url = reverse_lazy('store:product_list')
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
        url = reverse_lazy('store:product_manage', kwargs=dict(pk=self.product.pk))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200, response.data)
        self.assertEqual(response.data['id'], self.product.pk, response.data)

    def test_edit(self):
        url = reverse_lazy('store:product_manage', kwargs=dict(pk=self.product.pk))
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
        url = reverse_lazy('store:product_manage', kwargs=dict(pk=self.product.pk))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204, response.data)
        product = Product.objects.filter(pk=self.product.pk)  # type: Product
        self.assertIsNone(product.first())


class OrderViewTest(APITestCase):

    def setUp(self) -> None:
        self.product_1 = ProductFactory(title='P_1', amount=10)
        self.product_2 = ProductFactory(title='P_2', amount=10)
        self.product_3 = ProductFactory(title='P_3', amount=10)

    def test_list(self):
        OrderFactory()
        url = reverse_lazy('store:orders_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200, response.data)
        self.assertEqual(len(response.data), Order.objects.all().count(), response.data)

    def test_create(self):
        url = reverse_lazy('store:orders_list')

        # Продажа 1
        data = {
            'status': 'ordered',
            'products': [
                {
                    'product': 1,
                    'quantity': 10,
                    'price': 150
                },
                {
                    'product': 2,
                    'quantity': 5,
                    'price': 350
                }
            ]
        }
        response = self.client.post(url, data=json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 201, response.data)
        self.assertEqual(Order.objects.filter(pk=response.data['id']).count(), 1, response.data)

        # Продажа 2
        url = reverse_lazy('store:orders_list')
        data = {
            'status': 'ordered',
            'products': [
                {
                    'product': 1,
                    'quantity': 1,
                    'price': 150
                },
                {
                    'product': 2,
                    'quantity': 5,
                    'price': 350
                },
                {
                    'product': 3,
                    'quantity': 5,
                    'price': 450
                }
            ]
        }
        response = self.client.post(url, data=json.dumps(data), content_type="application/json")
        self.assertEqual(response.status_code, 204, response.data)
        self.assertEqual(response.data['enough_products'], False, response.data)

    def test_retrieve(self):
        order = OrderFactory(status=Status.ORDERED)
        url = reverse_lazy('store:order_manage', kwargs=dict(pk=order.pk))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200, response.data)
        self.assertEqual(response.data['id'], order.pk, response.data)

    def test_destroy(self):
        order = OrderFactory(status=Status.ORDERED)
        url = reverse_lazy('store:order_manage', kwargs=dict(pk=order.pk))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204, response.data)
        order = Order.objects.filter(pk=order.pk).first()
        self.assertEqual(order.status, Status.CANSELED, response.data)
