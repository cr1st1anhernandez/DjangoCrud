from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    path('users/', views.user_list, name='user_list'),
    path('users/create/', views.user_create, name='user_create'),
    path('users/<int:pk>/delete/', views.user_delete, name='user_delete'),

    path('products/', views.product_list, name='product_list'),
    path('products/<int:pk>/', views.product_detail, name='product_detail'),
    path('products/create/', views.product_create, name='product_create'),
    path('products/<int:pk>/edit/', views.product_edit, name='product_edit'),
    path('products/<int:pk>/delete/', views.product_delete, name='product_delete'),

    path('history/', views.history_list, name='history_list'),
    path('history/<int:pk>/', views.history_detail, name='history_detail'),

    # Carrito de compras
    path('cart/', views.cart_view, name='cart_view'),
    path('cart/add/<int:pk>/', views.cart_add, name='cart_add'),
    path('cart/remove/<int:pk>/', views.cart_remove, name='cart_remove'),
    path('cart/update/<int:pk>/', views.cart_update_quantity, name='cart_update_quantity'),
    path('cart/clear/', views.cart_clear, name='cart_clear'),

    # Ventas
    path('sales/', views.sale_list, name='sale_list'),
    path('sales/<int:pk>/', views.sale_detail, name='sale_detail'),
    path('sales/process/', views.sale_process, name='sale_process'),
    path('sales/ticket/<int:pk>/', views.sale_ticket, name='sale_ticket'),
]
