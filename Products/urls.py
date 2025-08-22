# urls.py

from django.urls import path
from .views import product_list
from . import views

urlpatterns = [
    path('products/', product_list , name='product_list'),
    path('products/<int:product_id>/', views.product_detail, name='product_detail'),
    path('categories/', views.category_list, name='category_list'),
    path('category/<int:category_id>/', views.category_detail, name='category_detail'),
    path('enroll/<int:product_id>/', views.enroll_in_course, name='enroll_in_course'),
]
