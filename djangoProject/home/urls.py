from django.urls import path, re_path
from . import views

app_name = 'home'
urlpatterns = [
    path('', views.home, name='home'),
    path('product', views.all_product, name='product'),
    path('detail/<int:id>', views.product_detail, name='detail'),
    path('category/<slug>/<int:id>/', views.all_product, name='category'),
    path('like/<int:id>/', views.product_like, name='product_like'),
    path('dislike/<int:id>/', views.product_dislike, name='product_dislike'),
    path('dislike/<int:id>/', views.product_dislike, name='product_dislike'),
    path('comment/<int:id>/', views.product_comment, name='product_comment'),
    path('reply/<int:id>/<int:comment_id>/', views.product_reply, name='product_reply'),
    path('like_comment/<int:id>/', views.comment_like, name='comment_like'),
    path('dislike_comment/<int:id>/', views.comment_dislike, name='comment_dislike'),
    path('search/', views.product_search, name='product_search'),
    path('favourite/<int:id>', views.favourite_product, name='favourite'),
    path('contact/', views.contact, name='contact'),
]
