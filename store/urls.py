from django.urls import path
from .views import *


urlpatterns = [
    path('',homepageview,name='home'),
    path('search/', search_view, name='search'),
    path('products-list/',productpageview,name='products'),
    path('products/<slug:slug>/',productdetailview,name='product-desc'),
    path('product/<slug:slug>/review/', add_review, name='add_review'),
    path('offers/',offerspageview,name='offers'),
    path('about/',aboutpageview,name='about'),
    path('contact/',contactpageview,name='contact'),
    path('return-policy/',returnpageview,name='return'),
    path('cart/', cart_detail, name='cart_detail'),
    path('cart/add/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:product_id>/', remove_from_cart, name='remove_from_cart'),
    path('cart/remove/<int:product_id>/<str:size>/', remove_from_cart, name='remove_from_cart_with_size'),
    path('cart/update/<int:product_id>/', update_cart, name='update_cart'),
    path('cart/update/<int:product_id>/<str:size>/', update_cart, name='update_cart_with_size'),
    path('checkout/', checkout, name='checkout'),
    path('checkout/process/', process_order, name='process_order'),
    path('order/success/<int:order_id>/', order_success, name='order_success'),
    path('orders/<int:order_id>/', order_details, name='order_details'),
    path('buy-now/<int:product_id>/', buy_now, name='buy_now'),
]