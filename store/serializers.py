from decimal import Decimal

from rest_framework import serializers

from store.models import Collection, Product


class CollectonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title',]


class ProductSerializer(serializers.ModelSerializer):
    price_with_tax = serializers.SerializerMethodField(
        method_name='calculate_tax')

    def calculate_tax(self, product):
        return product.unit_price * Decimal(0.2)

    class Meta:
        model = Product
        fields = ['id', 'title', 'unit_price', 'price_with_tax', 'collection']
