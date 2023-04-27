from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Collection, Product, Reviews
from .serializers import (CollectionSerializer, ProductSerializer,
                          ReviewSerializer)


# Create your views here.
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def perform_destroy(self, instance):
        if instance.orderitem_set.exists():
            return Response({'error': 'There are some order items associated with this product that you should delete first.'},
                            status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().perform_destroy(instance)


class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.prefetch_related('product_set').all()
    serializer_class = CollectionSerializer

    def perform_destroy(self, instance):
        if instance.product_set.exists():
            return Response({'error': "There are some product associated with this collection that you should delete first."},
                            status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().perform_destroy(instance)


class ReviewViewSet(ModelViewSet):
    queryset = Reviews.objects.all()
    serializer_class = ReviewSerializer
