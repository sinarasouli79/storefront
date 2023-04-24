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


    # def create(self, validated_data):
    #     product = Product.objects.create(**validated_data)
    #     product.other = '?'
    #     product.save()
    #     return product

    # def update(self, instance, validated_data):
    #     instance.unit_price = validated_data['unit_price']
    #     instance.save()
    #     return instance
    class Meta:
        model = Product
        fields = ['id', 'title', 'description','unit_price', 'inventory', 'price_with_tax', 'collection']
