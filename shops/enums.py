from enum import Enum
from django.db import models
from django.utils.translation import gettext_lazy as _

class ORDER_STATUS(models.TextChoices):
    CONFIRMED = "CONFIRMED", _("confirmed")
    PROCESS = "PROCESS", _("process")
    READY = "READY", _("ready")
    SERVED = "SERVED", _("served")
    CANCELLED = "CANCELLED",("cancelled")
    PLACE = "PLACE ",_("place")

