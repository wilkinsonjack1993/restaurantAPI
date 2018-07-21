from rest_framework import serializers
from .models import Order
from django.contrib.postgres.fields import ArrayField

# Order serializer mapping between JSON and model.
class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ('order_id', 'table_number', 'menu_items', 'time_stamp_entered', 'order_complete',)
        read_only_fields = ('order_id', 'time_stamp_entered',)
        extra_kwargs = {'table_number': {'required': False}}


    # Create a new order instance, populate it with the table number and menu items ordered and save.
    # The only fields set here are the table number and the menu items for the order as order complete will
    # default to false and the timestamp and order id will be automatically populated.
    def create(self, validated_data):
        new_order = Order()
        new_order.table_number = validated_data.get('table_number')
        new_order.menu_items = validated_data.get('menu_items')

        new_order.save()
        return new_order


    # For simplicity, on update we only mark an order as complete or not. If a user wishes to change an order, 
    # then an initial work around can be for a manager to delete the order and a customer to re-enter the order. 
    def update(self, instance, validated_data):
        instance.order_complete = validated_data.get('order_complete', instance.order_complete)
        instance.save()
        return instance


    


        
        


        
