"""
URL configuration for Shop_ir project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from Shop_ir.views import home, password_reset_confirm_view
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('' , home , name="home" ),
    path('Account/', include('Account.urls')),
    path('About/', include('About.urls')),
    path('Blog/', include('Blog.urls')),
    path('Products/', include('Products.urls')),
    path('Contact_us/', include('Contact_us.urls')),
    # فرم بازیابی رمز عبور برای کاربران
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='password_reset_form.html'),
         name='password_reset'),

    # پیامی که پس از ارسال فرم بازیابی رمز عبور نمایش داده می‌شود
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),
         name='password_reset_done'),

    # صفحه تنظیم رمز عبور جدید
    path('reset/<uidb64>/<token>/', password_reset_confirm_view, name='password_reset_confirm'),

    # پیامی که پس از تغییر موفقیت‌آمیز رمز عبور نمایش داده می‌شود
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
         name='password_reset_complete'),
]

handler404 = 'Shop_ir.views.custom_404'

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)