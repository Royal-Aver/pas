from django.contrib import admin

from products.models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "price",
        "discount",
        "quantity",
        "category",
        )
    list_editable = (
        "price",
        "discount",
        )
    search_fields = ("title", )
    list_filter = ("category", "price")
    fields = (
        "title",
        ("price", "discount",),
        "description",
        "quantity",
        "image",
        "slug",
        "category")
    prepopulated_fields = {"slug": ("title",)}
