from django.db import models
import uuid
from shops.enums import ORDER_STATUS, OrderPlace
from django.utils import timezone


# Create your models here.
class TimeStamp(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Restaurant(models.Model):
    pass


class Category(TimeStamp):
    name = models.CharField(max_length=200)
    status = models.BooleanField(default=0)
    is_delete = models.BooleanField(default=0)
    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE, related_name="category_restaurant"
    )

    def __str__(self) -> str:
        return self.name


class SubCategory(TimeStamp):
    name = models.CharField(max_length=200)
    native = models.CharField(max_length=200)
    status = models.BooleanField(default=0)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="subcategory_categoryname"
    )
    is_delete = models.BooleanField(default=0)

    def __str__(self) -> str:
        return self.name


class Item(TimeStamp):
    name = models.CharField(max_length=200)
    native = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.FloatField(default=0, blank=True, null=True)
    unit = models.CharField(max_length=10, default="")
    item_logo = models.ImageField(upload_to="item_logo", null=True, blank=True)
    status = models.BooleanField(default=1)
    is_delete = models.BooleanField(default=0)
    subcategory = models.ForeignKey(
        SubCategory, on_delete=models.CASCADE, related_name="subcategory"
    )

    def __str__(self) -> str:
        return self.name


class RestaurantTable(TimeStamp):
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name="restauranttable_restaurant",
        null=True,
        blank=True,
    )
    table_name = models.CharField(max_length=20, null=True, blank=True)
    is_new_ordered_place = models.BooleanField(default=False)
    qr_code = models.FileField(null=True, blank=True, help_text="Qr Code Field")
    order_uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    description = models.TextField(default="", null=True, blank=True)
    order_place = models.CharField(
        max_length=12,
        choices=OrderPlace.choices,
        default=OrderPlace.DIRECT_ORDER,
    )


class RestaurantTableSession(models.Model):
    """RestaurantTableSession Object is represent to a single customer based on Qrcode Scan

    Keyword arguments:
    argument --
    Return: return_description
    """

    restaurant_table = models.ForeignKey(
        RestaurantTable, on_delete=models.CASCADE, related_name="tablesession_table"
    )
    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE, related_name="tablesession_restaurant"
    )
    session_uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    session_index = models.IntegerField(null=True, blank=True)
    session_nickname = models.CharField(max_length=200, null=True, blank=True)
    session_pin = models.CharField(max_length=6)
    is_bill_paid = models.BooleanField(default=False)
    paid_by = models.ForeignKey(
        "payment.PaymentMethod",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="paid_by",
    )
    no_of_ordered_placed = models.IntegerField(default=0)
    no_of_ordered_confirmed = models.IntegerField(default=0)
    session_order_number = models.CharField(
        max_length=20, null=True, blank=True, help_text="bill number"
    )
    is_session_active = models.BooleanField(
        default=True, help_text="once object is created it autometically is active"
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    item_count = models.IntegerField(default=0)
    no_of_cancelled_order = models.IntegerField(default=0)
    email = models.EmailField(null=True)
    phone_number = models.CharField(null=True, max_length=20)
    name = models.CharField(max_length=50, null=True, blank=True)
    total_tip = models.FloatField(default=0)
    device_id = models.CharField(max_length=500, null=True)
    bill_type = models.BooleanField(default=False)
    delivery_charge = models.FloatField(default=float(0), null=True, blank=True)
    last_order_number = models.IntegerField(default=0)  # Track the last order number

    def __str__(self):
        return f"Table Session {self.id}"


class RestaurantTableSessionItem(models.Model):
    table_session = models.ForeignKey(
        RestaurantTableSession,
        on_delete=models.CASCADE,
        related_name="sessionitem_tablesession",
    )
    item = models.ForeignKey(
        Item, on_delete=models.CASCADE, related_name="sessionitem_item"
    )
    item_count = models.IntegerField()
    item_total_price = models.FloatField()
    item_unit = models.CharField(max_length=10, default="")
    item_price = models.FloatField()
    status = models.CharField(
        max_length=255,
        choices=OrderPlace.choices,
        default=OrderPlace.TABLE_ORDER.value,
    )


class OfferType(models.Model):
    name = models.CharField(max_length=100)


class Offer(TimeStamp):
    """
    Keyword arguments:
    argument -- In this model where user allow to select multiple item
    and set each item different price for speficific date
    or from_date to end_date
    Return: return_description
    Example: Today Offer this 3 item you get in 199
    """

    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE, related_name="offers"
    )
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    offer_type = models.ForeignKey(OfferType, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    # Fields specific to each offer type
    discount_percentage = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True
    )
    buy_quantity = models.IntegerField(null=True, blank=True)
    get_quantity = models.IntegerField(null=True, blank=True)
    applicable_products = models.ManyToManyField(Item, related_name="offers")

    def __str__(self) -> str:
        return self.name

    def is_valid(self):
        today = timezone.now().date()
        return self.is_active and (
            self.start_date <= today <= self.end_date
            if self.end_date
            else self.start_date <= today
        )
