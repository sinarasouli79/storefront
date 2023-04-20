from django.contrib import admin, messages
from django.db.models import Count
from django.urls import reverse
from django.utils.html import format_html
from django.utils.http import urlencode

from . import models

# Register your models here.


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership', 'orders_count']
    list_editable = ['membership']
    list_per_page = 10
    search_fields = ['first_name__istartswith', 'last_name__istartswith']
    ordering = ['first_name', 'last_name']

    @admin.display(ordering='orders_count')
    def orders_count(self, customer):
        url = (reverse('admin:store_order_changelist')
               + '?'
               + urlencode({'customer__id': customer.id}))
        return format_html(f"<a href={url}>{customer.orders_count}</a>")

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(orders_count=Count('order'))


class inventory_status(admin.SimpleListFilter):
    title = 'inventory'
    parameter_name = 'inventory'
    less_than_ten = '<10'

    def lookups(self, request, model_admin):
        return [(self.less_than_ten, 'low')]

    def queryset(self, request, queryset):
        if self.value() == self.less_than_ten:
            return queryset.filter(inventory__lt=10)


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    actions = ['clear_inventory']
    list_display = ['id', 'title', 'unit_price',
                    'inventory_status', 'collection', 'last_update']
    list_editable = ['unit_price']
    list_filter = ['collection', 'last_update', inventory_status]
    list_per_page = 10
    ordering = ['title', 'unit_price']

    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        return f'{product.inventory} (Low)' if product.inventory < 10 else f'{product.inventory} (Ok)'

    @admin.action(description='Clear inventory')
    def clear_inventory(self, request, queryset):
        update_count = queryset.update(inventory=0)
        self.message_user(request, f'{update_count} product(s) sucessfully updated.',
                          messages.ERROR)


@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'products_count']
    ordering = ['title']
    list_per_page = 10

    @admin.display(ordering='products_count')
    def products_count(self, collection):
        url = (reverse('admin:store_product_changelist')
               + '?'
               + urlencode({'collection__id': collection.id}))
        return format_html(f"<a href={url}>{collection.products_count}</a>")

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(products_count=Count('product'))


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['payment_status', 'placed_at', 'customer']
    list_per_page = 10


@admin.register(models.OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product',
                    'product_description', 'quantity', 'unit_price']
    list_select_related = ['order', 'product']
    list_per_page = 10

    @admin.display(ordering='product__description')
    def product_description(self, orderitem):
        return orderitem.product.description
