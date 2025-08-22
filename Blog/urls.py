# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.blog_list, name='blog_list'),
    path('<int:blog_id>/', views.blog_detail, name='blog_detail'),
    path('blog/<int:blog_id>/', views.blog_detail, name='blog_detail'),
    path('category/<int:category_id>/', views.category_blogs, name='category_blogs'),
    path('search/', views.search_blogs, name='search_blogs'),
]
