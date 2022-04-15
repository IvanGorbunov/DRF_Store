from rest_framework import status
from rest_framework.response import Response

from store.models import Product
from store.serializers import ProductListSerializer, ProductDetailSerializer, ProductUpdateSerializer
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
