from django.contrib import admin
from django.contrib.admin import ModelAdmin

from django.utils.translation import gettext_lazy as _

from store.models import Product


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
