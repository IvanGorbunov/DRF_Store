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

    def __str__(self):
        return f'Заказ: {self.pk}'

    def destroy(self):
        """
        Удаление заказа
        """
        # Удалить все заказанные продукты
        self.products.all().delete()

    def save_products(self, products):
        ids = []
        if products is None:
            return

        for product in products:
            product_id = product['product'].id
            instance, _ = OrderItem.objects.update_or_create(
                order=self,
                product=product['product'],
                quantity=product['quantity'],
                price=product['price'],
            )
            ids.append(instance.id)
            # TODO: реализовать расчет себестоимости
            # уменьшим на количество купленного
            amount = Product.objects.filter(pk=product_id).values('amount')[0]['amount']
            amount -= product['quantity']
            Product.objects.filter(pk=product_id).update(amount=amount)

        OrderItem.objects.filter(order=self).exclude(pk__in=ids).delete()


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