from django.contrib import admin
# Register your models here.
from django.contrib.contenttypes.admin import GenericTabularInline

from store.admin import ProductAdmin
from store.models import Product
from tags.models import TaggedItem


class TagInline(GenericTabularInline):
    extra = 0
    model = TaggedItem


class CustomProductAdmin(ProductAdmin):
    inlines = list(ProductAdmin.inlines) + [TagInline]


admin.site.unregister(Product)
admin.site.register(Product, CustomProductAdmin)
