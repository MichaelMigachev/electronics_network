from django.contrib import admin
from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "email",
        "first_name",
        "last_name",
        "phone",
        "is_active",
        "date_joined",
        "last_login",
    )
    search_fields = ("email",)
