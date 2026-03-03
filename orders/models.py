from django.db import models

from users.models import User
from products.models import Product


class Order(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Пользователь")
    created_timestamp =models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания")
    phone_number = models.CharField(
        max_length=20,
        verbose_name="Номер телефона")
    requires_delivery = models.BooleanField(
        default=False,
        verbose_name="Требуется доставка")
    delivery_adress = models.TextField(
        null=True,
        blank=True,
        verbose_name="Адрес доставки")
    payment_on_get = models.BooleanField(
        default=False,
        verbose_name="Оплата наличными")
    is_paid = models.BooleanField(
        default=False,
        verbose_name="Оплачен")
    status = models.CharField(
        max_length=50,
        default="В обработке",
        verbose_name="Статус")

    class Meta:
        db_table = "orders"
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return f"Заказ № {self.pk} | {self.user.first_name} {self.user.last_name}"


class OrderItemQuerySet(models.QuerySet):
    def total_price(self):
        return sum(item.total_price() for item in self)

    def total_quantity(self):
        return sum(item.quantity for item in self)


class OrderItem(models.Model):
    order = models.ForeignKey(
        to=Order,
        on_delete=models.CASCADE,
        verbose_name="Заказ")
    product = models.ForeignKey(
        to=Product,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Товар")
    name =models.CharField(
        max_length=255,
        verbose_name="Наименование"
    )
    price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        verbose_name="Цена")
    quantity = models.PositiveSmallIntegerField(
        default=0,
        verbose_name="Количество")
    created_timestamp = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата добавления")

    object = OrderItemQuerySet.as_manager()

    class Meta:
        db_table = "order_items"
        verbose_name = "Товар в заказе"
        verbose_name_plural = "Товары в заказе"

    def __str__(self):
        return f"{self.name} | {self.quantity} | Заказ № {self.order.pk}"

    def products_price(self):
        return round(self.price * self.quantity, 2)
