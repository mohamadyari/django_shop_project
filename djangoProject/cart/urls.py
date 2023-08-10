from django.urls import path
from . import views

app_name = 'cart'
urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),
    path('add/<int:id>/', views.add_cart, name='add_cart'),
    path('remove/<int:id>/', views.remove_cart, name='remove_cart'),
    path('add_single/<int:id>/', views.add_single, name='add_single'),
    path('remove_single/<int:id>/', views.remove_single, name='remove_single'),
    path('compare/<int:id>/', views.compare, name='compare'),
    path('show/', views.show, name='show'),
]