from django.db import transaction
from rest_framework import serializers

from store.models import Product, Order, OrderItem


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


class ProductUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            'id',
            'cost_price',
            'price',
            'amount',
        )

    @transaction.atomic()
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


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


class OrderListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = (
            'id',
            'status',
            'create_dt',
            'change_dt',
        )


class OrderItemEditSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = OrderItem
        fields = (
            'id',
            'order',
            'product',
            'quantity',
            'price',
        )


class OrderDetailSerializer(serializers.ModelSerializer):
    products = OrderItemEditSerializer(many=True, required=False, write_only=True)

    class Meta:
        model = Order
        fields = (
            'id',
            'status',
            'create_dt',
            'change_dt',

            'products',
        )

    @transaction.atomic()
    def create(self, validated_data):
        products = validated_data.pop('products', None)
        order = super().create(validated_data)  # type: Order
        order.save_products(products)
        return order
