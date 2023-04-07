"""Order views module"""
from rest_framework import generics
from rest_framework.exceptions import PermissionDenied

from orders.models import Order
from orders.serializers import OrderSerializer


class OrderAPIList(generics.ListCreateAPIView):
    """
    Returns list of orders in JSON format and gave an option to create orders
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderAPIUpdate(generics.RetrieveUpdateDestroyAPIView):
    """
    Returns distinct order JSON info and gave an option to update and delete it
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def put(self, request, *args, **kwargs):
        """Add a possibility of partial update, using put method"""
        return self.partial_update(request, *args, **kwargs)

    def perform_destroy(self, instance):
        """Protect order from delete if its status is 'accepted'."""
        if instance.status == 'accepted':
            raise PermissionDenied(
                detail="You can not delete orders with status 'accepted'."
            )
        instance.delete()
