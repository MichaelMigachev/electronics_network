from django.urls import path
from rest_framework.routers import DefaultRouter

from trading.views import (
    ContactInfoViewSet, ProductViewSet, VendorUpdateAPIView,
    VendorViewSet, VendorCreateAPIView, VendorListAPIView,
    VendorRetrieveAPIView, VendorDestroyAPIView
)
from users.apps import UsersConfig


app_name = UsersConfig.name

router = DefaultRouter()
router.register(r'contacts', ContactInfoViewSet, basename='contacts')
router.register(r'products', ProductViewSet, basename='products')
router.register(r'vendors', VendorViewSet, basename='vendors')

urlpatterns = [
    path("vendors/create/", VendorCreateAPIView.as_view(), name="vendor_create"),
    path("vendors/", VendorListAPIView.as_view(), name="vendors_list"),
    path("vendors/<int:pk>/", VendorRetrieveAPIView.as_view(), name="vendor_retrieve",),
    path("vendors/update/<int:pk>/", VendorUpdateAPIView.as_view(), name="vendor_update"),
    path("vendors/destroy/<int:pk>/", VendorDestroyAPIView.as_view(), name="vendor_destroy"),
]

urlpatterns += router.urls
