from django.db import transaction
from django.views.generic import ListView
from rest_framework import status
from rest_framework.response import Response

from store.filters import ReportFilter
from store.models import Product, Order, OrderItem
from store.products_in_stock import check_rest_products, return_of_products, get_report
from store.serializers import ProductListSerializer, ProductDetailSerializer, ProductUpdateSerializer, \
    OrderListSerializer, OrderDetailSerializer, OrderItemEditSerializer
from store.utils import MultiSerializerViewSet


class ProductViewSet(MultiSerializerViewSet):
    queryset = Product.objects.all()
    serializers = {
        'list': ProductListSerializer,
        'create': ProductDetailSerializer,
        'retrieve': ProductDetailSerializer,
        'update': ProductUpdateSerializer,
        'partial_update': ProductUpdateSerializer,
    }

    def list(self, request, *args, **kwargs):
        """
        Список продуктов
        """
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """
        Создание продукта
        """
        return super().create(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """
        Просмотр продукта
        """
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """
        Полное редактирование продукта
        """
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        """
        Частичное редактироание продукта
        """
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        Удаление продукта
        """
        product = self.get_object()
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class OrderViewSet(MultiSerializerViewSet):
    queryset = Order.objects.all()
    serializers = {
        'list': OrderListSerializer,
        'create': OrderDetailSerializer,
        'retrieve': OrderDetailSerializer,
        'destroy': OrderDetailSerializer,
    }

    def list(self, request, *args, **kwargs):
        """
        Список заказов
        """
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """
        Создание заказа
        """
        # Контроль остатков на складе
        context = check_rest_products(request.data['products'])
        if not context['enough_products']:
            return Response(context, status=status.HTTP_204_NO_CONTENT)
        return super().create(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """
        Просмотр заказа
        """
        order = self.get_object()  # type: Order
        serializer = OrderDetailSerializer(order)
        context = dict(serializer.data)
        return Response(context, status=status.HTTP_200_OK)

    @transaction.atomic()
    def destroy(self, request, *args, **kwargs):
        """
        Удаление заказа
        """
        order = self.get_object()  # type: Order
        order.destroy()
        # возврат товаров на склад
        products = OrderItem.objects.filter(order=order).all()
        serializer = OrderItemEditSerializer(products, many=True)
        return_of_products([dict(item) for item in serializer.data])
        return Response(status=status.HTTP_204_NO_CONTENT)


class ReportViewSet(MultiSerializerViewSet):
    queryset = Order.objects.all()
    filtersets = {
        'list': ReportFilter,
    }
    serializers = {
        'list': OrderDetailSerializer,
    }

    def list(self, request, *args, **kwargs):
        """
        Просмотр отчета
        """
        queryset = self.filter_queryset(self.get_queryset())
        products = get_report(queryset)

        context = {
            'products': products,
        }

        return Response(context, status=status.HTTP_200_OK)


class OrderListView(ListView):
    model = Order
    paginate_by = 100

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        new_context = {
            'object_list': [],
        }
        for order in context['object_list']:    # type Order
            serializer = OrderDetailSerializer(order)
            new_context['object_list'].append(serializer.data)
        return new_context


class OrderProductsListView(ListView):
    model = OrderItem
    paginate_by = 100

    def get_context_data(self, **kwargs):
        # queryset = OrderItem.objects.filter(order=)
        context = super().get_context_data(**kwargs)
        new_context = {
            'object_list': [],
        }
        # for order in context['object_list']:    # type Order
        #     serializer = OrderDetailSerializer(order)
        #     new_context['object_list'].append(serializer.data)
        return new_context
