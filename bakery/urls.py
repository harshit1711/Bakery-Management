from django.urls.conf import path

from . import views

urlpatterns = [
    path('register/', views.UserCreate.as_view(),name='register'),
    path('products/',
         views.AvailableProductsView.as_view(), name='products'),

]