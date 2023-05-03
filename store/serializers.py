from decimal import Decimal

from rest_framework import serializers

from store.models import Cart, Collection, Product, Review


class CollectionSerializer(serializers.ModelSerializer):
    products_count = serializers.IntegerField(
        read_only=True, source='product_set.count')

    class Meta:
        model = Collection
        fields = ['id', 'title', 'products_count']


class ProductSerializer(serializers.ModelSerializer):
    price_with_tax = serializers.SerializerMethodField(
        method_name='calculate_tax')

    def calculate_tax(self, product):
        return product.unit_price * Decimal(0.2)

    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'unit_price',
                  'inventory', 'price_with_tax', 'collection']


class ReviewSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        product = self.context['product']
        return Review.objects.create(product_id=product, **validated_data)

    class Meta:
        model = Review
        fields = ['id', 'name', 'description', 'date']


class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)

    class Meta:
        model = Cart
        fields = ['id']
