from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from .models import *


class ProductViewSetTests(APITestCase):
    """
    Тесты для ProductViewSet.

    Эти тесты проверяют CRUD операции для модели Product:
    - создание
    - получение
    - обновление
    - удаление
    - уменьшение количества товара
    """

    def setUp(self):
        """Настройка тестовой среды: создание начальных данных для тестов."""

        self.category = Category.objects.create(
            name="Test Category", description="A category for testing"
        )
        self.product = Product.objects.create(
            name="Test Product",
            quantity=10,
            barcode="1234567890123",
            category=self.category,
        )
        self.product2 = Product.objects.create(
            name="Test Product2",
            quantity=10,
            barcode="1234567890199",
            category=self.category,
        )

    def test_create_product(self):
        """Проверяет создание нового товара и увеличение количества товаров в базе."""

        url = reverse("product-list")
        data = {
            "name": "New Product",
            "quantity": 20,
            "barcode": "9876543210987",
            "category": self.category.id,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 3)
        product = Product.objects.get(name=data["name"])
        self.assertEqual(product.name, data["name"])
        self.assertEqual(product.quantity, data["quantity"])
        self.assertEqual(product.barcode, data["barcode"])
        self.assertEqual(product.category.id, data["category"])

    def test_get_product_list(self):
        """Проверяет количество товаров в базе."""

        url = reverse("product-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_product_detail(self):
        """Проверяет успешное получение товара."""

        url = reverse("product-detail", args=[self.product.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.product.name)

    def test_update_product(self):
        """Проверяет обновление существующего товара."""

        url = reverse("product-detail", args=[self.product.id])
        data = {
            "name": "Updated Product",
            "quantity": 15,
            "barcode": "1234567890123",
            "category": self.category.id,
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product.refresh_from_db()
        self.assertEqual(self.product.name, "Updated Product")

    def test_delete_product(self):
        """Проверяет успешное удаление товара."""

        url = reverse("product-detail", args=[self.product.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.count(), 1)
        
        self.assertFalse(Product.objects.filter(id=self.product.id).exists())

    def test_reduce_quantity_success(self):
        """Проверяет успешное уменьшение количества товара."""

        url = reverse("product-reduce-quantity", args=[self.product2.id])
        data = {"amount": 5}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product2.refresh_from_db()
        self.assertEqual(self.product2.quantity, 5)

    def test_reduce_quantity_error(self):
        """Проверяет обработку ошибок при попытке уменьшения количества на недопустимую величину."""

        url = reverse("product-reduce-quantity", args=[self.product.id])
        data = {"amount": -30}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("detail", response.data)


class PriceViewSetTests(APITestCase):
    """
    Тесты для PriceViewSet.

    Эти тесты проверяют CRUD операции для модели Price:
    - создание
    - получение
    - обновление
    - удаление
    """

    def setUp(self):
        """Настройка тестовой среды: создание начальных данных для тестов."""
        self.product = Product.objects.create(
            name="Test Product",
            quantity=10,
            barcode="1234567890123",
            category=None,
        )
        self.price = Price.objects.create(currency="USD", amount=100.57, product=self.product)
        self.price2 = Price.objects.create(currency="RUB", amount=1000.00, product=self.product)

    def test_get_price_detail(self):
        """Проверяет успешное получение цены товара"""

        url = reverse("price-detail", args=[self.price.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["amount"], str(self.price.amount))
        self.assertEqual(response.data["currency"], self.price.currency)

    def test_get_price_list(self):
        """Проверяет количество цен в базе."""

        url = reverse("price-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_price(self):
        """Проверяет создание новоой цены и увеличение количества цен в базе."""
        url = reverse("price-list")
        data = {"currency": "EUR", "amount": 85.50, "product": self.product.id}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Price.objects.count(), 3)

    def test_update_price(self):
        """Проверяет обновление существующей цены."""

        url = reverse("price-detail", args=[self.price.id])
        data = {"currency": "USD", "amount": 110.00, "product": self.product.id}
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.price.refresh_from_db()
        self.assertEqual(self.price.amount, 110.00)

    def test_delete_price(self):
        """Проверяет успешное удаление цены."""

        url = reverse("price-detail", args=[self.price.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Price.objects.count(), 1)


class CategoryViewSetTests(APITestCase):
    """
    Тесты для CategoryeViewSet.

    Эти тесты проверяют CRUD операции для модели Category:
    - создание
    - получение
    - обновление
    - удаление
    """

    def setUp(self):
        """Настройка тестовой среды: создание начальных данных для тестов."""

        self.category = Category.objects.create(
            name="Test Category1", description="A category for testing1"
        )
        self.category2 = Category.objects.create(
            name="Test Category2", description="A category for testing2"
        )

    def test_get_category_detail(self):
        """Проверяет успешное получение категории товара."""

        url = reverse("category-detail", args=[self.category.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.category.name)

    def test_get_category_list(self):
        """Проверяет количество категорий в базе."""
        url = reverse("category-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_category(self):
        """Проверяет создание новой категории и увеличение количества категорий в базе."""

        url = reverse("category-list")
        data = {"name": "Test Category3", "description": "A category for testing3"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 3)

    def test_update_category(self):
        """Проверяет обновление существующей категории."""

        url = reverse("category-detail", args=[self.category.id])
        data = {"name": "Updated Category", "description": "A category for testing2"}
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.category.refresh_from_db()
        self.assertEqual(self.category.name, "Updated Category")

    def test_delete_category(self):
        """Проверяет успешное удаление категории."""

        url = reverse("category-detail", args=[self.category.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Category.objects.count(), 1)
