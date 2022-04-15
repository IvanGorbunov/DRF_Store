from string import ascii_lowercase

from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyText, FuzzyFloat

from store.models import Product


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
