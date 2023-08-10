from django.urls import path
from . import views

app_name = 'account'
urlpatterns = [
    path('register/', views.user_register, name='user_register'),
    path('logout', views.log_out, name='log_out'),
    path('login/', views.user_login, name='user_login'),
    path('profile/', views.user_profile, name='user_profile'),
    path('update/', views.user_update, name='user_update'),
    path('change/', views.change_password, name='change_password'),
    path('login_phone/', views.phone, name='phone'),
    path('verify/', views.verify, name='verify'),
    path('active/<uidb64>/<token>/', views.RegisterEmail.as_view(), name='active'),
    path('reset', views.ResetPassword.as_view(), name='reset'),
    path('reset/done', views.DonePassword.as_view(), name='reset_done'),
    path('confirm/<uidb64>/<token>/', views.ConfirmPassword.as_view(), name='password_reset_confirm'),
    path('confirm/done/', views.Complete.as_view(), name='complete'),
    path('favourite/', views.favourite, name='favourite'),
    path('history/', views.history, name='history'),
    path('view/', views.product_view, name='product_view'),
]
