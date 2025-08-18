from rest_framework import viewsets, generics
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from trading.models import ContactInfo, Product, Vendor
from trading.serializers import ContactInfoSerializer, ProductSerializer, VendorUpdateSerializer, VendorSerializer
from trading.paginators import Paginator


class ContactInfoViewSet(viewsets.ModelViewSet):
    """
    API endpoint  для управления контактной информацией.
    """
    queryset = ContactInfo.objects.all()
    serializer_class = ContactInfoSerializer
    pagination_class = Paginator

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ('email', 'country', 'city')
    search_fields = ('email', 'country', 'city',)
    ordering_fields = ('email', 'country', 'city',)


class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint для управления продуктами.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = Paginator

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ('title', 'model')
    search_fields = ('title', 'model',)
    ordering_fields = ('title', 'model',)


# class VendorUpdateAPIView(generics.UpdateAPIView):
#     """API endpoint для обновления конкретного поставщика."""
#     serializer_class = VendorUpdateSerializer
#     queryset = Vendor.objects.all()


class VendorViewSet(viewsets.ModelViewSet):
    """API endpoint для управления поставщиками."""
    queryset = Vendor.objects.all().order_by('id')
    # queryset = Vendor.objects.all()
    # serializer_class = VendorSerializer
    pagination_class = Paginator

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ('title', 'level', 'debt_to_supplier')
    search_fields = ('title', 'level', 'debt_to_supplier')
    ordering_fields = ('title', 'level', 'debt_to_supplier')

    def get_serializer_class(self):
        if self.action == 'update':
            return VendorUpdateSerializer
        return VendorSerializer


# class VendorCreateAPIView(generics.CreateAPIView):
#     """API endpoint for creating a new vendor."""
#     serializer_class = VendorSerializer
#
#
# class VendorListAPIView(generics.ListAPIView):
#     """API endpoint for listing all vendors."""
#     serializer_class = VendorSerializer
#     queryset = Vendor.objects.all()
#
#
# class VendorRetrieveAPIView(generics.RetrieveAPIView):
#     """API endpoint for retrieving a specific vendor."""
#     serializer_class = VendorSerializer
#     queryset = Vendor.objects.all()
#
#
# class VendorDestroyAPIView(generics.DestroyAPIView):
#     """API endpoint for deleting a specific vendor."""
#     serializer_class = VendorSerializer
#     queryset = Vendor.objects.all()
