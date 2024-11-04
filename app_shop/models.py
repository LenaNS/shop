from django.db import models


class Category(models.Model):
    """
    Модель категорий товаров.

    Поля
    ----
    name:
        Название категории.
    description:
        Описание категории.
    """

    name = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(blank=True, verbose_name='Описание')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Тип"
        verbose_name_plural = "Типы"



class Product(models.Model):
    """
    Модель товаров.

    Поля
    ----
    name:
        Название товара.
    price:
        Цена товара.
    quantity:
        Количество товара на складе.
    barcode:
        Штрихкод товара.
    updated_at:
        Дата обновления записи о товаре.
    category:
        Тип товара (категория).
    """

    name = models.CharField(max_length=100, verbose_name='Название')

    quantity = models.PositiveIntegerField(verbose_name='Количество')
    barcode = models.CharField(max_length=50, unique=True, verbose_name='Штрихкод')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, verbose_name='Тип')

    def reduce_quantity(self, amount):
        """
        Уменьшает количество товара на складе.

        Параметры
        ----------
        amount : int
            Количество, на которое необходимо уменьшить количество товара.
            Должно быть положительным числом и не превышать текущее количество товара.

        Исключения
        ----------
        ValueError
            Вызывается, если amount меньше или равно 0, или если amount
            превышает текущее количество товара на складе.
        """
        if amount <= 0:
            raise ValueError("Сумма уменьшения должна быть положительной.")
        if amount > self.quantity:
            raise ValueError("Недостаточно товара на складе.")
        self.quantity -= amount
        self.save()

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
    

class Price(models.Model):
    """
    Модель цен товаров.

    Поля
    ----
    currency:
        Валюта цены.
    amount:
        Стоимость товара.
    """

    currency = models.CharField(max_length=10, verbose_name='Валюта')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Стоимость')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')

    def __str__(self):
        return f"{self.amount} {self.currency}"
    
    class Meta:
        verbose_name = "Цена"
        verbose_name_plural = "Цены"