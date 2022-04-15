from store.models import Product
from store.serializers import ProductListSerializer, ProductDetailSerializer
from store.utils import MultiSerializerViewSet


class ProductViewSet(MultiSerializerViewSet):
    queryset = Product.objects.all()
    serializers = {
        'list': ProductListSerializer,
        'create': ProductDetailSerializer,
    }

    def create(self, request, *args, **kwargs):
        """
        Создание клиента
        """
        return super().create(request, *args, **kwargs)