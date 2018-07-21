from rest_framework.decorators import api_view
from .serializers import OrderSerializer
from .models import Order
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class CreateOrder(APIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def post(self, request, format=None):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)

    # def mark_order_as_complete(self, request, *args, **kwargs):
    #     instance =  self.get_object()
    #     instance.order_complete = True
    #     instance.save()

    #     serializer = self.get_serializer(instance)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_update(serializer)

    #     return Response(serializer.data)
