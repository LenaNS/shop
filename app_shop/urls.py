from rest_framework.routers import DefaultRouter
from django.urls import include, path

from .viewsets import *

router = DefaultRouter()
router.register(r'prices', PriceViewSet)
router.register(r'products', ProductViewSet)
router.register(r'categories', CategoryViewSet)


urlpatterns = [
    path("api/", include(router.urls)),
]
