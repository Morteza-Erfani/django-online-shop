from django.urls import include
from django.urls import path

from .views import ProductListView, productDetailView

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('<int:pk>/', productDetailView.as_view(), name='product_detail'),
]
