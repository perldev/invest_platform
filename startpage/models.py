from __future__ import unicode_literals

from django.db import models

# Create your models here.


class InvestLot(models.Model):
    amount = models.DecimalField(default="0.0", max_digits=10,
                                 decimal_places=4,
                                 verbose_name="Sum of invest")
    percent = models.DecimalField(default="0.0", max_digits=10, decimal_places=4,
                                  max_length=40, verbose_name="Sum of lot")
    date_get = models.DateTimeField(auto_now_add=False, null=True)
