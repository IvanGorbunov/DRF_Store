from django.urls import path

from store import views

app_name = 'store_view'

urlpatterns = [
    path('', views.OrderListView.as_view(), name='order-list'),

]
