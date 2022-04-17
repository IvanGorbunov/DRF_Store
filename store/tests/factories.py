from string import ascii_lowercase

from factory import SubFactory
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyText, FuzzyFloat, FuzzyChoice

from store.choices import Status
from store.models import Product, OrderItem, Order


class ProductFactory(DjangoModelFactory):
    """
    Фабрика Продукта
    """
    class Meta:
        model = Product

    title = FuzzyText(length=30, chars=ascii_lowercase)
    cost_price = FuzzyFloat(100, 200)
    price = FuzzyFloat(500, 1000)
    amount = FuzzyFloat(0, 1000)


class OrderFactory(DjangoModelFactory):
    """
    Фабрика Заказа
    """
    class Meta:
        model = Order

    status = FuzzyChoice(choices=Status.ITEMS)


class OrderItemFactory(DjangoModelFactory):
    """
    Фабрика Заказанного товара
    """
    class Meta:
        model = OrderItem

    order = SubFactory(OrderFactory)
    product = SubFactory(ProductFactory)
    quantity = FuzzyFloat(100, 200)
    price = FuzzyFloat(500, 1000)
