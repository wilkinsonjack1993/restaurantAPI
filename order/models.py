from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

# Order model containing all details of the model.
class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    table_number = models.IntegerField()
    # Menu items stored in array field to allow for multiple menu items per order.
    menu_items = ArrayField(models.IntegerField(), blank=True, default=[])
    time_stamp_entered = models.DateTimeField(auto_now_add=True)
    order_complete = models.BooleanField(default=False)

    class Meta:
        ordering = ('time_stamp_entered',)

 