from django.db import transaction
from rest_framework import serializers

from store.models import Product


class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            'id',
            'title',
            'cost_price',
            'price',
            'amount',
            'create_dt',
            'change_dt',
        )

    @transaction.atomic()
    def create(self, validated_data):
        return super().create(validated_data)


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            'id',
            'title',
            'cost_price',
            'price',
            'amount',
            'create_dt',
            'change_dt',
        )
