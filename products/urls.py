from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('product/<int:pk>/review/', views.product_detail, name='add_review'),
    path('product/<int:product_pk>/review/<int:review_pk>/edit/', views.edit_review, name='edit_review'),
    path('product/<int:product_pk>/review/<int:review_pk>/delete/', views.delete_review, name='delete_review'),
    
    # Admin-only URLs (redirects to admin panel)
    path('create/', views.product_create, name='product_create'),
    path('update/<int:pk>/', views.product_update, name='product_update'),
    path('delete/<int:pk>/', views.product_delete, name='product_delete'),
] 