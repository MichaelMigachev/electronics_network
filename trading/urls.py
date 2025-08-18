from rest_framework.routers import DefaultRouter

from trading.views import ContactInfoViewSet, ProductViewSet,  VendorViewSet

from trading.apps import TradingConfig


app_name = TradingConfig.name

router = DefaultRouter()
router.register(r'contacts', ContactInfoViewSet, basename='contacts')
router.register(r'products', ProductViewSet, basename='products')
router.register(r'vendors', VendorViewSet, basename='vendors')

urlpatterns = []

urlpatterns += router.urls
