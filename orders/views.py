"""Order views module"""
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import status as st
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.exceptions import MethodNotAllowed, NotFound
from rest_framework.decorators import api_view

from orders.models import Order, STATUS_CHOICES
from orders.serializers import OrderSerializer
from orders.pagination import CustomPagination


class OrderAPIList(generics.ListCreateAPIView):
    """
    Returns list of orders in JSON format and gave an option to create orders
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['external_id', 'status']
    ordering_fields = ['id', 'status', 'created_at']


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
            raise MethodNotAllowed(
                'delete',
                detail="You can not delete orders with status 'accepted'.",
            )
        instance.delete()


@api_view(['POST'])
def status_change(request, pk, status):
    """Change order status"""
    if status not in [x[0] for x in STATUS_CHOICES]:
        raise MethodNotAllowed(
            'post',
            detail="You can change order status"
                   " only to 'accepted' or 'failed'",
        )
    order = Order.objects.get(id=pk)
    if not order:
        raise NotFound(f'Product with id {pk} does not exist.')
    if order.status != 'new':
        raise MethodNotAllowed(
            'post',
            detail="You can not change order status if it is not 'new'",
        )
    order.status = status
    order.save()
    return Response(status=st.HTTP_200_OK)
