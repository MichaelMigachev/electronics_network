from django.contrib import admin, messages
from django.urls import reverse
from django.utils.html import format_html
from trading.models import ContactInfo, Product, Vendor


@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    """Класс для настройки отображения модели "ContactInfo"
    в административной панели"""

    list_display = (
        "pk",
        "email",
        "country",
        "city",
        "street",
        "house_number",
        "vendor_link",  # ссылка на поставщика
    )
    list_filter = ("city",)

    def vendor_link(self, obj):
        # Получаем связанного поставщика
        vendor = Vendor.objects.filter(contact=obj).first()
        if vendor:
            url = reverse("admin:trading_vendor_change", args=[vendor.pk])
            return format_html('<a href="{}">{}</a>', url, vendor.title)
        return "-"

    vendor_link.short_description = "Поставщик"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Класс для настройки отображения модели "Product"
    в административной панели"""

    list_display = (
        "pk",
        "title",
        "model",
        "launched_at",
    )
    list_filter = ("title",)


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    """Класс для настройки отображения модели "Vendor"
    в административной панели"""

    list_display = (
        "pk",
        "title",
        "get_level_display",  # Показываем читаемое значение level
        "debt_to_supplier",
        "contact_link",  # Ссылка на контактную информацию
        "supplier_link",  # Ссылка на поставщика
        "created_at",
    )
    list_filter = ("level", "created_at")
    search_fields = ("title", "contact__email")
    raw_id_fields = ("supplier",)  # Для удобного выбора поставщика
    actions = ["clear_debt_action"]

    def clear_debt_action(self, request, queryset):
        """Admin action для очистки задолженности перед поставщиком"""
        updated = queryset.update(debt_to_supplier=0)
        self.message_user(
            request,
            f"Задолженность очищена у " f"{updated} поставщиков",
            messages.SUCCESS,
        )

    clear_debt_action.short_description = "Очистить задолженность перед поставщиком"

    def contact_link(self, obj):
        url = reverse("admin:trading_contactinfo_change", args=[obj.contact.pk])
        return format_html('<a href="{}">{}</a>', url, obj.contact.email)

    contact_link.short_description = "Контактная информация"

    def supplier_link(self, obj):
        if obj.supplier:
            url = reverse("admin:trading_vendor_change", args=[obj.supplier.pk])
            return format_html('<a href="{}">{}</a>', url, obj.supplier.title)
        return "-"

    supplier_link.short_description = "Поставщик"
    # Для отображения продуктов в админке
    filter_horizontal = ("products",)
