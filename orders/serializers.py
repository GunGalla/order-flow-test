"""Serializers for orders"""
from rest_framework import serializers

from orders.models import Order


class OrderSerializer(serializers.ModelSerializer):
    """Serialize order to JSON"""

    class Meta:
        """Define model and fields to serialize"""
        model = Order
        fields = "__all__"
