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

    def validate(self, attrs):
        print("here****************")
        if not attrs['title'].__contains__('sina'):
            raise serializers.ValidationError('title should contain sina')
        return attrs

    class Meta:
        model = Product
        fields = ['id', 'title', 'unit_price', 'price_with_tax', 'collection']
