from decimal import Decimal

from rest_framework import serializers

from store.models import Collection, Product


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
