"""Admin panel module"""
from django.contrib import admin
from orders.models import Order, OrderDetail, Product

admin.site.register(Order)
admin.site.register(OrderDetail)
admin.site.register(Product)
