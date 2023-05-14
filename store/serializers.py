from decimal import Decimal

from django.db import transaction
from rest_framework import serializers

from .models import (Cart, CartItem, Collection, Customer, Order, OrderItem,
                     Product, Review, ProductImage)
from .signals import order_created


class ProductImageSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        validated_data['product_id'] = self.context['product_id']
        return super().create(validated_data)

    class Meta:
        model = ProductImage
        fields = ['id', 'image']


class ProductSerializer(serializers.ModelSerializer):
    price_with_tax = serializers.SerializerMethodField(
        method_name='calculate_tax')

    productimage_set = ProductImageSerializer(many=True, read_only=True)

    def calculate_tax(self, product):
        return product.unit_price * Decimal(0.2)

    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'unit_price',
                  'inventory', 'price_with_tax', 'collection', 'productimage_set']


class CollectionSerializer(serializers.ModelSerializer):
    products_count = serializers.IntegerField(
        read_only=True, source='product_set.count')

    class Meta:
        model = Collection
        fields = ['id', 'title', 'products_count']


class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'unit_price', ]


class ReviewSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        product = self.context['product']
        return Review.objects.create(product_id=product, **validated_data)

    class Meta:
        model = Review
        fields = ['id', 'name', 'description', 'date']


class CartItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, cartitem):
        return cartitem.quantity * cartitem.product.unit_price

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'total_price']


class AddCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()

    def validate_product_id(self, product_id):
        if not Product.objects.filter(pk=product_id).exists():
            raise serializers.ValidationError("product doen't exist")
        return product_id

    def save(self, **kwargs):
        cart_id = self.context['cart_pk']
        product_id = self.validated_data['product_id']

        try:
            cartitem = CartItem.objects.get(cart=cart_id, product=product_id)
            cartitem.quantity += self.validated_data['quantity']
            cartitem.save()
            self.instance = cartitem

        except CartItem.DoesNotExist:
            self.instance = CartItem.objects.create(
                cart_id=cart_id, **self.validated_data)

        return self.instance

    class Meta:
        model = CartItem
        fields = ['id', 'product_id', 'quantity']


class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['quantity']


class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    total_price = serializers.SerializerMethodField()
    items = CartItemSerializer(
        many=True, read_only=True, source='cartitem_set')

    def get_total_price(self, cart):
        return sum([item.product.unit_price * item.quantity for item in cart.cartitem_set.all()])

    class Meta:
        model = Cart
        fields = ['id', 'items', 'total_price']


class CustomerSrializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Customer
        fields = ['id', 'user_id', 'membership', 'birth_date', 'phone']


class OrderItemSerialzier(serializers.ModelSerializer):
    product = SimpleProductSerializer()

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'unit_price', 'quantity']


class OrderSrializer(serializers.ModelSerializer):
    orderitem_set = OrderItemSerialzier(many=True)

    class Meta:
        model = Order
        fields = ['id', 'customer', 'placed_at',
                  'payment_status', 'orderitem_set']


class AddOrderSerializer(serializers.Serializer):
    cart_id = serializers.UUIDField()

    def validate_cart_id(self, cart_id):
        if not Cart.objects.filter(pk=cart_id).exists():
            raise serializers.ValidationError(
                'not cart with given id was found')
        if not CartItem.objects.filter(cart_id=cart_id).exists():
            raise serializers.ValidationError('the cart is empty')
        return cart_id

    def save(self, **kwargs):
        with transaction.atomic():
            user_id = self.context['user_id']
            cart_id = self.validated_data['cart_id']
            customer = Customer.objects.get(user_id=user_id)
            order = Order.objects.create(customer=customer)
            orderitems = [
                OrderItem(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    unit_price=item.product.unit_price
                ) for item in Cart.objects.get(id=cart_id).cartitem_set.all()
            ]

            OrderItem.objects.bulk_create(orderitems)

            Cart.objects.filter(pk=cart_id).delete()

            order_created.send_robust(self.__class__, order=order)

            return order


class UpdateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['payment_status']
