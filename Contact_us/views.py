from django.shortcuts import render, redirect
from django.contrib import messages
from .models import ContactMessage


def contact_us(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')

        # بررسی تعداد کلمات وارد شده
        name_parts = full_name.split(" ", 1)
        if len(name_parts) == 1:
            first_name = name_parts[0]
            last_name = ""  # اگر فقط یک کلمه وارد شد، فیلد نام خانوادگی خالی خواهد ماند
        else:
            first_name, last_name = name_parts

        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        # ذخیره اطلاعات به دیتابیس
        ContactMessage.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            message=message
        )

        # اضافه کردن پیام موفقیت
        messages.success(request, 'پیام شما با موفقیت ارسال شد. از تماس شما متشکریم.')

        return redirect('contact_us')  # هدایت به صفحه اصلی فرم
    return render(request, 'contact_us.html')

