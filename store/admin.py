from django.contrib import admin
from django.contrib.admin import ModelAdmin

from store.models import Product


@admin.register(Product)
class ProductAdmin(ModelAdmin):
    verbose_name_plural = 'Номенклатура'
    list_display = (
        'id',
        'title',
        'cost_price',
        'price',
        'amount',
    )
    list_display_links = (
        'id',
        'title',
    )
