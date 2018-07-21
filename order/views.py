from rest_framework.decorators import api_view
from .serializers import OrderSerializer
from .models import Order
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User


class CreateOrder(APIView):

    def post(self, request, format=None):
        
        try:
            print(request.user.username)
            user = User.objects.get(username=request.user.username)
            
            if(user.is_staff == False):
                return self.insert_order(request)
            return Response("Staff cannot enter orders", status=status.HTTP_400_BAD_REQUEST)
            
        except User.DoesNotExist:
            return Response("User does not exist",status=status.HTTP_400_BAD_REQUEST)
            

    def insert_order(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)
    

class ManageOrder(APIView):

    def get_object(self, pk):
        try:
            return Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            raise Http404

    def put(self, request, pk, format=None):
        try:
            user = User.objects.get(username=request.user)
            if(user.is_staff == True):
                order = self.get_object(pk)
                serializer = OrderSerializer(order, data=request.data)

                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)

            return Response("Only staff can change orders", status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response("User does not exist", status=status.HTTP_400_BAD_REQUEST)
        


    def get(self, request, pk, format=None):
        order = self.get_object(pk=pk)
        print(order)
        serializer = OrderSerializer(order, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print(serializer._errors)
            return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request,pk, format=None):
        try:
            user = User.objects.get(username=request.user)
            if(user.is_superuser == True):
                order = self.get_object(pk=pk)
                order.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response("Only managers can delete orders", status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response("User does not exist", status=status.HTTP_400_BAD_REQUEST)


