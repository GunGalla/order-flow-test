"""Serializers for orders"""
from rest_framework import serializers
from rest_framework.exceptions import MethodNotAllowed

from orders.models import Order, OrderDetail, Product


class ProductSerializer(serializers.ModelSerializer):
    """Serialize product to JSON"""
    id = serializers.IntegerField()

    class Meta:
        """Define related model and fields to serialize"""
        model = Product
        fields = ['id', 'name']
        read_only_fields = ['name']


class OrderDetailSerializer(serializers.ModelSerializer):
    """Serialize order details to JSON"""
    product = ProductSerializer()

    class Meta:
        """Define related model and fields to serialize"""
        model = OrderDetail
        fields = ['id', 'product', 'amount', 'price']

    def validate_product(self, value):
        """Check existence of posted product"""
        product_id = value['id']
        if Product.objects.filter(id=product_id).exists():
            return value
        raise serializers.ValidationError(
            f'Product with id {product_id} does not exist.'
        )


class OrderSerializer(serializers.ModelSerializer):
    """Serialize order to JSON"""
    created_at = serializers.DateTimeField(
        format="%d-%m-%YT%H:%M:%S",
        allow_null=True,
        read_only=True,
    )
    status = serializers.CharField(read_only=True)
    details = OrderDetailSerializer(many=True)

    class Meta:
        """Define related model and fields to serialize"""
        model = Order
        fields = ['id', 'status', 'created_at', 'external_id', 'details']

    def create(self, validated_data):
        """Overriding default method to be able to write nested fields"""
        details_data = validated_data.pop('details')
        order = Order.objects.create(**validated_data)
        for order_detail in details_data:
            product_id = order_detail.pop('product')['id']
            product = Product.objects.get(id=product_id)
            OrderDetail.objects.create(
                order=order,
                product=product,
                **order_detail
            )
        return order

    def update(self, instance, validated_data):
        """
        Protect orders with statuses different for 'new' from updating.
        Also saving only changes in 'external_id' field.
        """
        if instance.status != 'new':
            raise MethodNotAllowed(
                'put',
                detail="You can not change orders "
                       "with status different from 'new'.",
            )
        instance.external_id = validated_data.get(
            'external_id',
            instance.external_id
        )
        instance.save()
        return instance
