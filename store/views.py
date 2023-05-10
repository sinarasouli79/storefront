from django_filters.rest_framework.backends import DjangoFilterBackend
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from . import serializers
from .filters import ProductFilter
from .models import Cart, CartItem, Collection, Customer, Product, Review
from .pagination import DefaultPagination
from .permissions import FullDjangoModelPermissions, IsAdminOrReadOnly

# Create your views here.


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = serializers.ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    ordering_fields = ['title', 'unit_price']
    pagination_class = DefaultPagination
    permission_classes = [IsAdminOrReadOnly]
    search_fields = ['title', 'description']

    def perform_destroy(self, instance):
        if instance.orderitem_set.exists():
            return Response({'error': 'There are some order items associated with this product that you should delete first.'},
                            status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().perform_destroy(instance)


class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.prefetch_related('product_set').all()
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = serializers.CollectionSerializer

    def perform_destroy(self, instance):
        if instance.product_set.exists():
            return Response({'error': "There are some product associated with this collection that you should delete first."},
                            status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().perform_destroy(instance)


class ReviewViewSet(ModelViewSet):
    serializer_class = serializers.ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(product=self.kwargs['product_pk'])

    def get_serializer_context(self):

        return {'product': self.kwargs['product_pk']}


class CartViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.DestroyModelMixin,
                  GenericViewSet):

    queryset = Cart.objects.prefetch_related('cartitem_set__product').all()
    serializer_class = serializers.CartSerializer


class CartItemViewSet(ModelViewSet):

    http_method_names = ['post', 'get', 'patch', 'delete']

    def get_queryset(self):
        return CartItem.objects.select_related('product').filter(cart_id=self.kwargs['cart_pk'])

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.CartItemSerializer
        elif self.request.method == 'POST':
            return serializers.AddCartItemSerializer

        elif self.request.method == 'PATCH':
            return serializers.UpdateCartItemSerializer

    def get_serializer_context(self):
        return {'cart_pk': self.kwargs['cart_pk']}


class CustomerViewSet(ModelViewSet):

    queryset = Customer.objects.all()
    serializer_class = serializers.CustomerSrializer
    permission_classes = [FullDjangoModelPermissions]

    @action(detail=False, methods=['GET', 'PUT'], permission_classes=[IsAuthenticated])
    def me(self, request):
        (customer, created) = Customer.objects.get_or_create(pk=request.user.pk)
        if request.method == 'GET':
            serializer = serializers.CustomerSrializer(customer)
            return Response(serializer.data)

        elif request.method == 'PUT':
            serializer = serializers.CustomerSrializer(
                customer, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
