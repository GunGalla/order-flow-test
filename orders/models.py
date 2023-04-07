"""Order related models"""
from django.db import models

STATUS_CHOICES = (
        ('new', 'new'),
        ('accepted', 'accepted'),
        ('failed', 'failed'),
    )


class Order(models.Model):
    """Order model"""

    status = models.CharField(
        max_length=12,
        choices=STATUS_CHOICES,
        default='new',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    external_id = models.CharField(max_length=128, unique=True)


class Product(models.Model):
    """Product model"""

    name = models.CharField(max_length=64)


class OrderDetail(models.Model):
    """Distinct Order details"""

    order = models.ForeignKey(
        to=Order,
        on_delete=models.CASCADE,
        related_name='details',
    )
    amount = models.IntegerField()
    product = models.ForeignKey(
        to=Product,
        on_delete=models.CASCADE,
        related_name='product',
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
