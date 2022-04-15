from django.db import models

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
