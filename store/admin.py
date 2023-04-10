from django.contrib import admin
from . import models
from django.db.models import Count
# Register your models here.


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership']
    list_editable = ['membership']
    ordering = ['first_name', 'last_name']
    list_per_page = 10


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'unit_price', 'inventory_status']
    list_editable = ['unit_price']
    ordering = ['title', 'unit_price']
    list_per_page = 10

    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        return 'Low' if product.inventory else 'Ok'

@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'products_count']
    ordering = ['title']
    list_per_page = 10

    @admin.display(ordering='products_count')
    def products_count(self, collection):
        return collection.products_count
    

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(products_count=Count('product'))


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['payment_status', 'placed_at', 'customer']
    list_per_page = 10

@admin.register(models.OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'product_description', 'quantity', 'unit_price']
    list_select_related = ['order', 'product']
    list_per_page = 10

    @admin.display(ordering='product__description')
    def product_description(self, orderitem):
        return orderitem.product.description