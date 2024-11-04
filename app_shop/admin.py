from django.contrib.admin import ModelAdmin, register
from .models import *


@register(Product)
class ProductAdmin(ModelAdmin):
    """
    Панель администрирования товаров.

    Поля
    ----
    list_display:
        Список отображаемых полей.
    search_fields:
        Список полей по которым выполняется поиск.
    """
    
    list_display = (
        "name",
        "quantity",
        "barcode",
        "updated_at",
        "category",
    )
    search_fields = ['name', 'category__name']


@register(Category)
class CategoryAdmin(ModelAdmin):
    """
    Панель администрирования типа товаров.

    Поля
    ----
    list_display:
        Список отображаемых полей.
    """
    
    list_display = (
        "name",
        "description",
    )


@register(Price)
class PriceAdmin(ModelAdmin):
    """
    Панель администрирования цены товаров.

    Поля
    ----
    list_display:
        Список отображаемых полей.
    """
    
    list_display = (
        "currency",
        "amount",
        "product"
    )