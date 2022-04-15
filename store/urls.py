from django.urls import path

from store import views

app_name = 'store'

urlpatterns = [
    path('', views.ProductViewSet.as_view({'get': 'list', 'post': 'create'}), name='list'),
    path('<int:pk>/', views.ProductViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='manage'),
]
