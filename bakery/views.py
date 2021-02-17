# python imports
import datetime

# framework imports
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_200_OK
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

# app imports
from .models import Ingredient, BakeryItem, OrderItem, Order
from .serializers import *


# Create your views here.


class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)


class AvailableProductsView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = BakeryItem.objects.all()
    serializer_class = BakeryItemSerializer
    http_method_names = ['get']

    def get_queryset(self):
        return BakeryItem.objects.filter(is_available=True)


class PlaceOrderView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = OrderItemSerializer

    def create(self, request, *args, **kwargs):
        customer = request.user
        order_date = datetime.datetime.now()
        order_obj = Order.objects.create(customer=customer, order_date=order_date)

        order_items = []
        billing_amount = 0.0
        for data in request.data:
            try:
                item = BakeryItem.objects.get(id=data['item'])
                billing_amount += item.cost
            except ObjectDoesNotExist:
                return Response("Item does not exist in the bakery", status=HTTP_400_BAD_REQUEST)
            order_items_obj = OrderItem(order=order_obj, quantity=data['quantity'], item=item)
            order_items.append(order_items_obj)

        OrderItem.objects.bulk_create(order_items)

        return Response(f"Order placed , total payable amount : {billing_amount}", status=HTTP_201_CREATED)


class OrderHistory(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = OrderSerializer

    def get(self, request, *args, **kwargs):
        orders = Order.objects.filter(customer=self.request.user)
        order_items = OrderItem.objects.filter(order__in=orders).select_related('order').values()
        return Response(order_items, status=HTTP_200_OK)


class AddIngredientToBakery(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = IngredientSerializer

    def create(self, request, *args, **kwargs):
        ingredients = []
        for data in request.data:
            ingredients_obj = Ingredient(name=data['name'], flavour=data['flavour'], description=data['description'])
            ingredients.append(ingredients_obj)

        Ingredient.objects.bulk_create(ingredients)

        return Response(f"Ingredients added to bakery successfully", status=HTTP_201_CREATED)


class BakeryItemView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = BakeryItemSerializer
    queryset = BakeryItem.objects.all()

    def get(self, request, *args, **kwargs):
        bakery_item = BakeryItem.objects.all()
        data = []
        for item in bakery_item:
            value_dict = {'ingredient': item.ingredient.all().values(),
                          'quantity': item.quantity,
                          'cost_price': item.cost_price,
                          'selling_price': item.selling_price, 'is_available': item.is_available
                          }

            data.append(value_dict)

        return Response(data, status=HTTP_200_OK)





