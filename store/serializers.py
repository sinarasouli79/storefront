from decimal import Decimal

from rest_framework import serializers

from store.models import Collection


class CollectonSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=255)


class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=255)
    unit_price = serializers.DecimalField(max_digits=6, decimal_places=2)
    # price = serializers.DecimalField(max_digits=6, decimal_places=2, source='unit_price')
    prce_with_tax = serializers.SerializerMethodField(
        method_name='calculate_tax')

    # collection = serializers.PrimaryKeyRelatedField(
    #     queryset=Collection.objects.all())
    # collection = serializers.StringRelatedField()
    # collection = CollectonSerializer()
    collection = serializers.HyperlinkedRelatedField(queryset = Collection.objects.all(),view_name='collection-detail')

    def calculate_tax(self, product):
        return product.unit_price * Decimal(0.2)
