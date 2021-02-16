from django.contrib import admin

# Register your models here.

from .models import BakeryItem
from .models import Ingredient
from .models import OrderItem
from.models import Order


admin.site.register(BakeryItem)
admin.site.register(Ingredient)
admin.site.register(Order)
admin.site.register(OrderItem)
