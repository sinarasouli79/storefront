from django.contrib import admin, messages
from django.db.models import Count
from django.urls import reverse
from django.utils.html import format_html
from django.utils.http import urlencode

from . import models
# Register your models here.


class OrderInline(admin.TabularInline):
    extra = 0
    model = models.Order
    fields = ['payment_status', 'placed_at']
    readonly_fields = ['placed_at']


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    autocomplete_fields = ['user']
    inlines = [OrderInline]
    list_display = ['first_name', 'last_name', 'membership', 'orders_count']
    list_editable = ['membership']
    list_per_page = 10
    list_select_related = ['user',]
    search_fields = ['user__first_name__istartswith', 'user__last_name__istartswith']
    ordering = ['user__first_name', 'user__last_name']

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
    autocomplete_fields = ['collection']
    list_display = ['id', 'title', 'unit_price',
                    'inventory_status', 'collection', 'last_update']
    list_editable = ['unit_price']
    list_filter = ['collection', 'last_update', inventory_status]
    list_per_page = 10
    ordering = ['title', 'unit_price']
    prepopulated_fields = {'slug': ['title',]}
    readonly_fields = ['id', 'last_update']
    search_fields = ['title__istartswith']

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
    autocomplete_fields = ['featured_product']
    list_display = ['title', 'products_count']
    list_per_page = 10
    ordering = ['title']
    search_fields = ['title__istartswith']

    @admin.display(ordering='products_count')
    def products_count(self, collection):
        url = (reverse('admin:store_product_changelist')
               + '?'
               + urlencode({'collection__id': collection.id}))
        return format_html(f"<a href={url}>{collection.products_count}</a>")

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(products_count=Count('product'))


class OrderItemInline(admin.TabularInline):
    autocomplete_fields = ['product']
    extra = 0
    model = models.OrderItem


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    autocomplete_fields = ['customer']
    inlines = [OrderItemInline]
    list_display = ['payment_status', 'placed_at', 'customer']
    list_per_page = 10
    search_fields = ['customer__first_name__istartswith',
                     'customer__last_name__istartswith']


@admin.register(models.OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    autocomplete_fields = ['order', 'product']
    list_display = ['order', 'product',
                    'product_description', 'quantity', 'unit_price']
    list_select_related = ['order', 'product', 'order__customer']
    list_per_page = 10

    @admin.display(ordering='product__description')
    def product_description(self, orderitem):
        return orderitem.product.description
