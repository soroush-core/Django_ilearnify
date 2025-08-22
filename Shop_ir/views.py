from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.utils.http import urlsafe_base64_decode
from django.contrib import messages
from django.contrib.auth.models import User
from Products.models import Category, Product, Instructor
from django.db.models import Count


# index site
def home(request):
    instructors = Instructor.objects.all()
    categories = Category.objects.annotate(course_count=Count('products')).order_by('-id')[:8]
    latest_products = Product.objects.order_by('-created_at')[:6]
    query = request.GET.get('q', '')  # دریافت عبارت جستجو از URL
    products = Product.objects.all()

    total_products = Product.objects.count()
    total_instructors = Instructor.objects.count()
    total_users = User.objects.count()

    if query:
        # جستجو بر اساس نام محصول
        products = products.filter(name__icontains=query)

        # جستجو بر اساس تگ‌ها
        products = products.filter(tags__name__icontains=query)
    return render(request, 'home.html' , {'products': products, 'query': query , 'categories': categories ,
                                          'latest_products': latest_products,'instructors': instructors ,
                                          'total_products': total_products,
                                          'total_instructors': total_instructors,
                                          'total_users': total_users,
                                          })


def base_view(request):
    categories = Category.objects.all()
    return render(request, 'base.html', {'categories': categories})



def custom_404(request, exception):
    return render(request, '404.html', status=404)






def password_reset_confirm_view(request, uidb64, token):
    try:
        # دریافت uid از کد base64 شده
        uid = urlsafe_base64_decode(uidb64).decode()
        user = get_user_model().objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, user.DoesNotExist):
        user = None

    # بررسی اعتبار توکن
    if user and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            password1 = request.POST.get('new_password1')
            password2 = request.POST.get('new_password2')

            # بررسی مطابقت رمز عبور جدید
            if password1 and password2 and password1 == password2:
                user.set_password(password1)  # ذخیره رمز عبور جدید
                user.save()
                messages.success(request, "رمز عبور با موفقیت تغییر کرد.")
                return redirect('password_reset_complete')  # مسیری که پس از تغییر رمز عبور نمایش داده می‌شود
            else:
                messages.error(request, "رمز عبور و تایید آن باید یکسان باشند.")
        return render(request, 'password_reset_confirm.html')

    else:
        messages.error(request, "لینک بازیابی رمز عبور منقضی شده است یا معتبر نیست.")
        return redirect('password_reset')  # برگشت به صفحه بازیابی رمز عبور