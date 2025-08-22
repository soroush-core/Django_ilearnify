from django.urls import path
from . import views

urlpatterns = [
    # سایر URLها
    path('about-us/', views.about_us_view, name='about_us'),  # URL برای نمایش صفحه "درباره ما"
    path('faq/', views.faq_view, name='faq'),
]
