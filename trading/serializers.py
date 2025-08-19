from rest_framework.serializers import ModelSerializer

from trading.models import ContactInfo, Product, Vendor
from trading.validators import validate_hierarchy


class ContactInfoSerializer(ModelSerializer):
    """Serializer для контактной информации."""

    class Meta:
        model = ContactInfo
        fields = "__all__"


class ProductSerializer(ModelSerializer):
    """Serializer для продуктов."""

    class Meta:
        model = Product
        fields = "__all__"


class VendorSerializer(ModelSerializer):
    """
    Serializer для создания и чтения поставщиков.
    Включает вложенные Serializers для contact и products.
    """

    contact = ContactInfoSerializer()
    products = ProductSerializer(many=True)
    read_only_fields = ("debt_to_supplier",)

    class Meta:
        model = Vendor
        fields = "__all__"
        validators = [validate_hierarchy]


class VendorUpdateSerializer(ModelSerializer):
    """
    Serializer для обновления полей поставщика.
    """

    class Meta:
        model = Vendor
        fields = ("pk", "title", "level", "contact", "products", "debt_to_supplier")
        read_only_fields = (
            "pk",
            "created_at",
            "debt_to_supplier",
        )
        validators = [validate_hierarchy]
