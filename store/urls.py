from django.urls import path

from store import views

app_name = 'store_view'

urlpatterns = [
    path('', views.OrderListView.as_view(), name='order-list'),
    path('order/<int:pk>/', views.OrderProductsListView.as_view(), name='order-products'),
    path('order/<int:pk>/products/', views.OrderItemListView.as_view(), name='order-products'),
]
