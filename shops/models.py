from django.db import models
import uuid
from shops.enums import ORDER_STATUS


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
    restaurant = models.ForeignKey(Restaurant,on_delete=models.CASCADE, related_name="category_restaurant")

    def __str__(self) -> str:
        return self.name

class SubCategory(TimeStamp):
    name = models.CharField(max_length=200)
    native = models.CharField(max_length=200)
    status = models.BooleanField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="subcategory_categoryname")
    is_delete = models.BooleanField(default=0)


    def __str__(self) -> str:
        return self.name


class Item(TimeStamp):
    name = models.CharField(max_length=200)
    native = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.FloatField(default=0,blank=True,null=True)
    unit = models.CharField(max_length=10,default="")
    item_logo = models.ImageField(upload_to='item_logo',null=True,blank=True)
    status = models.BooleanField(default=1)
    is_delete = models.BooleanField(default=0)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name="subcategory")  

    def __str__(self) -> str:
        return self.name
    
class RestaurantTable(TimeStamp):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="restauranttable_restaurant",null=True, blank=True)
    table_name =models.CharField(max_length=20,null=True, blank=True)
    is_new_ordered_place = models.BooleanField(default=False)
    qr_code = models.FileField(null=True,blank=True,help_text="Qr Code Field")
    order_uuid = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        editable=False
    )
    description = models.TextField(default='', null=True, blank=True)
    """
    below filed are required to think again to create enums
    """
    # is_waiter_assigned = models.BooleanField(default=False)
    # is_pin_enable = models.BooleanField(default=False)
    # direct_order_table = models.BooleanField(default=False)
    # is_delete = models.BooleanField(default=False)
    # is_online_order = models.BooleanField(default=False)
    # bill_type = models.BooleanField(default=False)


class RestaurantTableSession(models.Model):
    """ RestaurantTableSession Object is represent to a single customer based on Qrcode Scan
    
    Keyword arguments:
    argument -- 
    Return: return_description
    """
    
    restaurant_table = models.ForeignKey(
        RestaurantTable, on_delete=models.CASCADE, 
        related_name='tablesession_table'
    )
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="tablesession_restaurant")    
    session_uuid = models.UUIDField(unique=True, default = uuid.uuid4,editable = False)
    session_index = models.IntegerField(null=True, blank=True)
    session_nickname = models.CharField(max_length=200, null=True, blank=True)

    #in session pin using use can merge bill so it not editable
    session_pin = models.CharField(
        max_length=6
    )

    is_bill_paid = models.BooleanField(default=False)

    # paid_by = models.ForeignKey(RestaurantBucket, null=True, blank=True, on_delete=models.CASCADE, related_name='session_paid_by')
    # discount = models.ForeignKey(RestaurantDiscount, null=True, blank=True, on_delete=models.CASCADE, related_name='session_discount')
    no_of_ordered_placed = models.IntegerField(default=0)
    no_of_ordered_confirmed = models.IntegerField(default=0)

    session_order_number = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        help_text="bill number"
    )
    is_session_active = models.BooleanField(
        default=True,help_text="once object is created it autometically is active"
    )
    amount = models.DecimalField(max_digits=10,decimal_places=2)
    is_payment_in_process = models.BooleanField(default=False)
    no_of_cancelled_order = models.IntegerField(default=0)
    email = models.EmailField(null=True)
    phone_number = models.CharField(null=True,max_length=20)
    name = models.CharField(max_length=50, null=True, blank=True)
    total_tip = models.FloatField(default=0)
    device_id = models.CharField(max_length=500, null=True)
    bill_type = models.BooleanField(default=False)
    delivery_charge = models.FloatField(
        default=float(0),null=True,blank=True
    )


class RestaurantTableSessionItem(models.Model):
    table_session = models.ForeignKey(
        RestaurantTableSession, 
        on_delete=models.CASCADE, 
        related_name="sessionitem_tablesession"
    )
    item = models.ForeignKey(
        Item, on_delete=models.CASCADE, 
        related_name="sessionitem_item"
    )
    item_count = models.IntegerField()
    item_total_price = models.FloatField()
    item_unit =models.CharField(max_length=10,default="")
    item_price = models.FloatField()
    status = models.CharField(
        max_length=255, choices=ORDER_STATUS.choices, 
        default=ORDER_STATUS.PLACE.value, null=True, blank=True
    )
     







    








    

