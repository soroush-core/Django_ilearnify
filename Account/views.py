from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib.auth import logout
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import CustomUser
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist



def register(request):
    if request.method == 'POST':
        # دریافت اطلاعات از فرم
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # ایجاد کاربر جدید
        user = User.objects.create_user(username=email, password=password, email=email)
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        # ایجاد CustomUser برای ذخیره اطلاعات اضافی
        custom_user = CustomUser.objects.create(user=user, first_name=first_name, last_name=last_name, email=email)
        custom_user.save()

        # ورود خودکار کاربر بعد از ثبت‌نام
        login(request, user)

        return redirect('home')  # بعد از ثبت‌نام به صفحه پروفایل برو

    return render(request, 'register.html')


@login_required
def user_profile(request):
    try:
        user = CustomUser.objects.get(user=request.user)
    except ObjectDoesNotExist:
        user = None

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        profile_image = request.FILES.get('profile_image')  # دریافت فایل آپلود شده

        # ذخیره تغییرات
        if user:
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            if profile_image:
                user.profile_image = profile_image  # ذخیره تصویر پروفایل جدید
            user.save()
            messages.success(request, 'تغییرات با موفقیت ذخیره شد.')
            return redirect('profile')  # هدایت به صفحه پروفایل پس از ذخیره تغییرات

    return render(request, 'profile.html', {'user': user})

def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            # پیدا کردن کاربر با ایمیل
            user = User.objects.get(email=email)

            # استفاده از authenticate برای احراز هویت کاربر با ایمیل و رمز عبور
            user = authenticate(request, username=user.email, password=password)

            if user is not None:
                # ورود به سیستم
                login(request, user)
                return redirect('home')  # هدایت به صفحه اصلی پس از ورود موفق
            else:
                messages.error(request, 'نام کاربری یا رمز عبور اشتباه است.')
        except User.DoesNotExist:
            messages.error(request, 'کاربری با این ایمیل پیدا نشد.')

    return render(request, 'login.html')  # قالب لاگین را رندر می‌کند

def logout_view(request):
    logout(request)
    return redirect('/')