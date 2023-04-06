"""Serializers for orders"""
from rest_framework import serializers

from orders.models import Order, OrderDetail, Product


class ProductSerializer(serializers.ModelSerializer):
    """Serialize product to JSON"""
    class Meta:
        """Define related model and fields to serialize"""
        model = Product
        fields = ['id', 'name']


class OrderDetailSerializer(serializers.ModelSerializer):
    """Serialize order details to JSON"""
    product = ProductSerializer(read_only=True)

    class Meta:
        """Define related model and fields to serialize"""
        model = OrderDetail
        fields = ['id', 'product', 'amount', 'price']


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
