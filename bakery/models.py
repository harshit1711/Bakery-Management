from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here.


class Ingredient(models.Model):
    name = models.CharField(max_length=256)
    flavour = models.CharField(max_length=256)
    description = models.TextField()


class BakeryItem(models.Model):
    ingredient = models.ManyToManyField(Ingredient, null=True, related_name='bakery')
    quantity = models.DecimalField(max_digits=10, decimal_places=3)
    cost_price = models.DecimalField(max_digits=10, decimal_places=3)
    selling_price = models.DecimalField(max_digits=10, decimal_places=3)
    is_available = models.BooleanField(default=True)


class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='order')
    order_date = models.DateTimeField(default=datetime.datetime.now())
    is_delivered = models.BooleanField(default=False)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, related_name='order_item')
    item = models.ForeignKey(BakeryItem, on_delete=models.CASCADE, null=True, related_name='orderitems')
    quantity = models.PositiveIntegerField(default=1)


