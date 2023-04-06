# from django.shortcuts import render
from rest_framework import generics

from orders.models import Order
from orders.serializers import OrderSerializer


class OrderAPIList(generics.ListCreateAPIView):
    """
    Returns list of orders in JSON format and gave an option to create orders
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
