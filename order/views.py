from rest_framework.decorators import api_view
from .serializers import OrderSerializer
from .models import Order
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User

# Views relating to non staff members.
class CreateOrder(APIView):

    # This is used to create an order. This is only possible if the user is not a member of staff.
    def post(self, request, format=None):
        
        try:
            user = User.objects.get(username=request.user.username)
            
            # Validate that the user is a customer.
            if(user.is_staff == False):
                return self.insert_order(request)
            return Response("Staff cannot enter orders", status=status.HTTP_400_BAD_REQUEST)
            
        except User.DoesNotExist:
            return Response("User does not exist",status=status.HTTP_400_BAD_REQUEST)
            
    # Method that will insert a new order into the database
    def insert_order(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)
    
# Class for staff to manage existing orders
class ManageOrder(APIView):

    # Get an order from the database that matches the given primary key
    def get_object(self, pk):
        try:
            return Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            raise Http404

    # Update an order, note that while not currently validated, the only possible field that can be update
    # with this method is order_completed (see serializer).
    # Orders can only be updated by members of staff.
    def put(self, request, pk, format=None):
        try:
            user = User.objects.get(username=request.user)
            if(user.is_staff == True):
                order = self.get_object(pk)
                serializer = OrderSerializer(order, data=request.data)

                # Check that serializer is valid and save updated order
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)

            return Response("Only staff can change orders", status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response("User does not exist", status=status.HTTP_400_BAD_REQUEST)
        

    # Get the order with the corresponding primary key - can be accessed by all users
    def get(self, request, pk, format=None):
        order = self.get_object(pk=pk)
        serializer = OrderSerializer(order, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print(serializer._errors)
            return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)

    # Delete order with corresponding primary key - this can only be done by managers (marked as superusers)
    def delete(self, request, pk, format=None):
        try:
            user = User.objects.get(username=request.user)
            if(user.is_superuser == True):
                order = self.get_object(pk=pk)
                order.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response("Only managers can delete orders", status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response("User does not exist", status=status.HTTP_400_BAD_REQUEST)


