# apps/products/urls.py

from django.urls import path
from .views import ProductCategoryListCreateView, ProductCategoryDetailView,ProductDetailAPIView,ProductListCreateAPIView,CustomerProductListCreateAPIView,CustomerProductDetailAPIView,ProductRecallAPIView

urlpatterns = [
    path('categories/', ProductCategoryListCreateView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', ProductCategoryDetailView.as_view(), name='category-detail'),
    path('products/', ProductListCreateAPIView.as_view(), name='product-list-create'),
    path('products/<int:pk>/', ProductDetailAPIView.as_view(), name='product-detail'),
    path('customer-products/', CustomerProductListCreateAPIView.as_view(), name='customerproduct-list-create'),
    path('customer-products/<int:pk>/', CustomerProductDetailAPIView.as_view(), name='customerproduct-detail'),
    path('product-recalls/', ProductRecallAPIView.as_view()),         # for list
    path('product-recalls/<int:pk>/', ProductRecallAPIView.as_view())
]
