from rest_framework.serializers import ValidationError


def validate_hierarchy(data):
    """Валидация иерархии объекта Vendor."""
    level = dict(data).get("level")
    supplier = dict(data).get("supplier")
    if supplier and level <= supplier.level:
        raise ValidationError(
            "Поставщик должен быть выше в иерархии"
        )
    elif level != 0:
        raise ValidationError(
            "При уровне больше 0 укажите поставщика."
        )
    return data
