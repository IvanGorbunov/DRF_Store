from django.db import models

from store.choices import Status
from store.utils import DateModelMixin


class Product(DateModelMixin):
    """
    Модель: Номенклатура
    """
    title = models.CharField('Название', max_length=250)
    cost_price = models.FloatField("Себестоимость", blank=True, default=0)
    price = models.FloatField("Цена", blank=True, default=0)
    amount = models.FloatField("Количество", blank=True, default=0)

    class Meta:
        verbose_name = 'Номенклатура'
        verbose_name_plural = 'Номенклатура'

    def __str__(self):
        return self.title + ' (' + str(self.pk) + ')'


class Order(DateModelMixin):
    """
    Модель: Заказ
    """
    status = models.CharField('Статус заказа', max_length=50, choices=Status.CHOICES, default=Status.ORDERED)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class OrderItem(models.Model):
    """
    Модель: Заказанный товар
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    quantity = models.PositiveIntegerField("Количество", blank=True, default=0)
    price = models.FloatField("Цена", blank=True, default=0)

    class Meta:
        verbose_name = 'Заказанный товар'
        verbose_name_plural = 'Заказанные товары'