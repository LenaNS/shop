from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .serializers import *
from .models import *

__all__ = ["ProductViewSet", "PriceViewSet", "CategoryViewSet"]


class ProductViewSet(ModelViewSet):
    """
    Представление для обработки CREATE, PUT, PATCH, GET (ALL), DELETE операций управления продуктами.

    Поля
    ----
    queryset: QuerySet[Product]
        Стандартный набор объектов Product.
    serializer_class:
        Стандартный используемый сериализатор.
    """

    queryset = Product.objects
    serializer_class = ProductSerializer

    def get_serializer_class(self):
        if self.action == "reduce_quantity":
            return ReduceQuantitySerializer
        return super().get_serializer_class()

    @action(detail=True, methods=["post"], url_name='reduce-quantity')
    def reduce_quantity(self, request, pk=None):
        """
        Обрабатывает запрос на уменьшение количества товара на складе.

        Параметры
        ----------
        request : 
            Объект запроса.
        pk : 
            Первичный ключ продукта.

        Возвращает
        ----------
        Response
            - При успешном выполнении: данные обновленного товара и статус 200 OK.
            - При ошибке: сообщение об ошибке и статус 400 Bad Request.
        """
        product = self.get_object()
        serializer = ReduceQuantitySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        amount = serializer.validated_data["amount"]
        try:
            product.reduce_quantity(amount)
            return Response(ProductSerializer(product).data, status=status.HTTP_200_OK)

        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class PriceViewSet(ModelViewSet):
    """
    Представление для обработки CREATE, PUT, PATCH, GET (ALL), DELETE операций управления ценами.

    Поля
    ----
    queryset: QuerySet[Price]
        Стандартный набор объектов Price.
    serializer_class:
        Стандартный используемый сериализатор.
    """

    queryset = Price.objects
    serializer_class = PriceSerializer


class CategoryViewSet(ModelViewSet):
    """
    Представление для обработки CREATE, PUT, PATCH, GET (ALL), DELETE операций управления типами товаров.

    Поля
    ----
    queryset: QuerySet[Category]
        Стандартный набор объектов Category.
    serializer_class:
        Стандартный используемый сериализатор.
    """

    queryset = Category.objects
    serializer_class = CategorySerializer
