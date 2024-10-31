from rest_framework.serializers import ModelSerializer, Serializer, IntegerField

from .models import *


__all__ = [
    "ProductSerializer", 
    "ReduceQuantitySerializer",
    "PriceSerializer",
    "CategorySerializer"
]

class ProductSerializer(ModelSerializer):
    """
    Сериализатор для GET (ALL), CREATE, PUT/PATCH, DELETE операций с объектами Product.
    """

    class Meta:
        """
        В сериализатор включены все поля.
        """

        model = Product
        fields = "__all__"


class PriceSerializer(ModelSerializer):
    """
    Сериализатор для GET (ALL), CREATE, PUT/PATCH, DELETE операций с объектами Price.
    """

    class Meta:
        """
        В сериализатор включены все поля.
        """

        model = Price
        fields = "__all__"



class ReduceQuantitySerializer(Serializer):

    amount = IntegerField(required=True)



class CategorySerializer(ModelSerializer):
    """
    Сериализатор для GET (ALL), CREATE, PUT/PATCH, DELETE операций с объектами Category.
    """

    class Meta:
        """
        В сериализатор включены все поля.
        """

        model = Category
        fields = "__all__"