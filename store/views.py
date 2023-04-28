from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Collection, Product, Review
from .serializers import CollectionSerializer, ProductSerializer, ReviewSerializer


# Create your views here.
class ProductViewSet(ModelViewSet):
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = Product.objects.all()
        collectoin_id = self.request.query_params.get('collection_id')
        if collectoin_id:
            queryset = queryset.filter(collection_id=collectoin_id)
        return queryset

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
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(product=self.kwargs['product_pk'])

    def get_serializer_context(self):

        return {'product': self.kwargs['product_pk']}
