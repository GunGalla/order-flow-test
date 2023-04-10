"""Order views module"""
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import status as st
from rest_framework import generics
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.exceptions import MethodNotAllowed, NotFound
from rest_framework.decorators import api_view

from orders.models import Order, STATUS_CHOICES
from orders.serializers import OrderSerializer
from orders.pagination import CustomPagination
from order_flow.settings import DEBUG


class OrderAPIListCreate(generics.ListCreateAPIView):
    """
    Returns list of orders in JSON format and gave an option to create orders
    """
    if DEBUG:
        renderer_classes = [JSONRenderer, BrowsableAPIRenderer]
    else:
        renderer_classes = [JSONRenderer]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['external_id', 'status']
    ordering_fields = ['id', 'status', 'created_at']


class OrderAPIRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    """
    Returns distinct order JSON info and gave an option to update and delete it
    """
    if DEBUG:
        renderer_classes = [JSONRenderer, BrowsableAPIRenderer]
    else:
        renderer_classes = [JSONRenderer]
    parser_classes = [JSONParser]
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
    try:
        order = Order.objects.get(id=pk)
    except Order.DoesNotExist:
        raise NotFound(f'Order with id {pk} does not exist.')

    if status not in [statuses[0] for statuses in STATUS_CHOICES]:
        raise MethodNotAllowed(
            'post',
            detail="You can change order status"
                   " only to 'accepted' or 'failed'",
        )
    if order.status != 'new':
        raise MethodNotAllowed(
            'post',
            detail="You can not change order status if it is not 'new'",
        )
    order.status = status
    order.save()
    return Response(status=st.HTTP_200_OK)
