# urls.py
from django.urls import path
from . import views
from .views import logout_view


urlpatterns = [
    path('register/', views.register, name='register'),
    path('profile/', views.user_profile, name='profile'),
    path('login/', views.user_login, name='login'),
    path('logout/', logout_view, name='logout'),
]
