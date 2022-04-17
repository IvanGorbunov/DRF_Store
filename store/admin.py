from django.contrib import admin
from django.contrib.admin import ModelAdmin, TabularInline

from store.models import Product, Order, OrderItem


@admin.register(Product)
class ProductAdmin(ModelAdmin):
    verbose_name_plural = 'Номенклатура'
    list_display = (
        'create_dt',
        'id',
        'title',
        'cost_price',
        'price',
        'amount',
        'change_dt',
    )
    list_per_page = 25
    fieldsets = (
        (
            None, {
                'fields': (
                    'title',
                    'cost_price',
                    'price',
                    'amount',
                )
            }
        ),
    )
    list_display_links = (
        'id',
        'title',
    )


class OrderItemAInline(TabularInline):
    raw_id_fields = ('product', )
    model = OrderItem
    extra = 0
    verbose_name_plural = 'Товары'


@admin.register(Order)
class OrderAdmin(ModelAdmin):
    inlines = (
        OrderItemAInline,
    )

    verbose_name_plural = 'Заказ'
    list_display = (
        'id',
        'status',
        'create_dt',
        'change_dt',
    )
    list_per_page = 25
    fieldsets = (
        (
            None, {
                'fields': (
                    'status',
                )
            }
        ),
    )
    list_display_links = (
        'id',
    )


@admin.register(OrderItem)
class OrderItemAdmin(ModelAdmin):

    verbose_name_plural = 'Заказанный товар'
    list_display = (
        'id',
        'order',
        'product',
        'quantity',
        'price',
    )
    list_per_page = 25
    fieldsets = (
        (
            None, {
                'fields': (
                    'order',
                    'product',
                    'quantity',
                    'price',
                )
            }
        ),
    )
    list_display_links = (
        'id',
    )
