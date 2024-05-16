from django.db import models
from uuid import uuid4


# Create your models here.
class Timestamp(models.Model):
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Creation Date")
    updated_date = models.DateTimeField(auto_now=True, verbose_name="Last Updated")

    class Meta:
        abstract = True
        ordering = ["-created_date"]
        verbose_name = "Timestamp"
        verbose_name_plural = "Timestamps"

    def __str__(self):
        return f"Created on {self.created_date}, updated on {self.updated_date}"


class PaymentMethod(Timestamp):
    name = models.CharField(max_length=200, verbose_name="Payment Method Name")

    class Meta:
        verbose_name = "Payment Method"
        verbose_name_plural = "Payment Methods"

    def __str__(self):
        return self.name
