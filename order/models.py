from django.db import models
from django.contrib.postgres.fields import ArrayField

class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    table_number = models.IntegerField()
    menu_items = ArrayField(models.IntegerField(), blank=True, default=[])
    time_stamp_entered = models.DateTimeField(auto_now_add=True)
    order_complete = models.BooleanField(default=False)

    class Meta:
        ordering = ('time_stamp_entered',)