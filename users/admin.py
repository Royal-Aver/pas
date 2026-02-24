from django.contrib import admin

from users.models import User
from carts.models import Cart


class CartTabAdmin(admin.TabularInline):
    model = Cart
    fields = (
        "product",
        "quantity",
        "created_timestamp")
    readonly_fields = ("created_timestamp",)
    extra = 1


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",)

    inlines = [CartTabAdmin,]
