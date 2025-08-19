from rest_framework import viewsets, serializers
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from trading.models import ContactInfo, Product, Vendor
from trading.serializers import (
    ContactInfoSerializer,
    ProductSerializer,
    VendorUpdateSerializer,
    VendorSerializer,
)
from trading.paginators import Paginator


class ContactInfoViewSet(viewsets.ModelViewSet):
    """
    API endpoint  для управления контактной информацией.
    """

    queryset = ContactInfo.objects.all()
    serializer_class = ContactInfoSerializer
    pagination_class = Paginator

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    # f
    filterset_fields = {
        "email": ["exact", "icontains"],
        "country": ["exact", "icontains"],
        "city": ["exact", "icontains"],
    }
    search_fields = (
        "email",
        "country",
        "city",
    )
    ordering_fields = (
        "email",
        "country",
        "city",
    )


class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint для управления продуктами.
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = Paginator

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ("title", "model")
    search_fields = (
        "title",
        "model",
    )
    ordering_fields = (
        "title",
        "model",
    )


class VendorViewSet(viewsets.ModelViewSet):
    """API endpoint для управления поставщиками."""

    queryset = Vendor.objects.all().order_by("id")
    pagination_class = Paginator

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    # filter_fields = ('title', 'level', 'debt_to_supplier')
    filterset_fields = {
        "title": ["exact", "icontains"],
        "level": ["exact"],
        "contact__country": ["exact", "icontains"],  # фильтр по стране
    }
    search_fields = ("title", "level", "debt_to_supplier")
    ordering_fields = ("title", "level", "debt_to_supplier")

    def get_serializer_class(self):
        if self.action == "update":
            return VendorUpdateSerializer
        return VendorSerializer

    def perform_update(self, serializer):
        # Дополнительная защита на уровне view
        if "debt_to_supplier" in serializer.validated_data:
            raise serializers.ValidationError(
                {"detail": "Изменение задолженности запрещено"}
            )
        serializer.save()
