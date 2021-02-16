from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse
from .models import *
from .serializers import *
from django.views.generic.base import View
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated

from .serializers import UserSerializer


# Create your views here.


class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)


class AvailableProductsView(generics.ListCreateAPIView):
    # permission_classes = (IsAuthenticated,)
    queryset = BakeryItem.objects.all()
    serializer_class = BakeryItemSerializer
    http_method_names = ['get']


