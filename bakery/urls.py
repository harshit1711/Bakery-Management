from django.urls.conf import path

from . import views

urlpatterns = [
    path('register/', views.UserCreate.as_view(), name='register'),
    path('bakery-available-products/',
         views.AvailableProductsView.as_view(), name='products'),
    path('place-order/',
         views.PlaceOrderView.as_view(), name='order'),
    path('order-history/', views.OrderHistory.as_view(), name='order_history'),
    path('add-ingredients/', views.AddIngredientToBakery.as_view(), name='ingredients'),
    path('bakery/', views.BakeryItemView.as_view(), name='bakery'),
]