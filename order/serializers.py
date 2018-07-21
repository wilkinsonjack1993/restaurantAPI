from rest_framework import serializers
from .models import Order
from django.contrib.postgres.fields import ArrayField


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ('order_id', 'table_number', 'menu_items', 'time_stamp_entered', 'order_complete',)
        read_only_fields = ('order_id', 'time_stamp_entered',)


    order_id = serializers.IntegerField(read_only=True)
    table_number = serializers.IntegerField()
    menu_items = ArrayField(serializers.IntegerField(), blank=True, default=[])
    time_stamp_entered = serializers.DateTimeField(read_only=True)
    order_complete = serializers.BooleanField(default=False)

    # Create a new order instance, populate it with the table number and menu items ordered and save.
    def create(self, validated_data):
        new_order = Order()
        new_order.table_number = validated_data.get('table_number')
        new_order.menu_items = validated_data.get('menu_items')

        new_order.save()
        return new_order


    # Update the model
    def update(self, instance, validated_data):
        instance.order_complete = validated_data.get('order_complete', instance.order_complete)
        instance.table_number = validated_data.get('table_number', instance.table_number)
        instance.menu_items = validated_data.get('menu_items', instance.menu_items)
        instance.save()
        return instance


    


        
        


        
