"""Serializers for orders"""
from rest_framework import serializers

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
