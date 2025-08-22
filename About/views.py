from django.shortcuts import render
from .models import AboutUs, FAQ


def about_us_view(request):
    about_us = AboutUs.objects.first()  # فرض می‌کنیم فقط یک صفحه درباره ما داریم
    return render(request, 'About.html', {'about_us': about_us})



def faq_view(request):
    faqs = FAQ.objects.all()  # گرفتن تمام سوالات متداول از دیتابیس
    return render(request, 'fag.html', {'faqs': faqs})
