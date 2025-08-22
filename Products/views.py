from django.core.paginator import Paginator
from django.shortcuts import render
from .models import Product, Category, Enrollment
from django.shortcuts import get_object_or_404
from django.shortcuts import render, get_object_or_404
from .models import Video

def product_list(request):
    product_list = Product.objects.all()

    # فیلتر بر اساس قیمت
    price_filter = request.GET.get('price')
    if price_filter == 'free':
        product_list = product_list.filter(is_free=True)
    elif price_filter == 'paid':
        product_list = product_list.filter(is_free=False)

    # فیلتر بر اساس سطح محصول
    level_filter = request.GET.get('level')
    if level_filter:
        product_list = product_list.filter(level=level_filter)

    # فیلتر بر اساس دسته‌بندی
    category_filter = request.GET.get('category')
    if category_filter and category_filter != 'all':
        product_list = product_list.filter(category__name=category_filter)

    # جستجو بر اساس نام یا تگ
    search_query = request.GET.get('search')
    if search_query:
        # جستجو در نام محصول و تگ‌ها
        product_list = product_list.filter(name__icontains=search_query) | product_list.filter(tags__name__icontains=search_query)

    # جلوگیری از تکرار محصولات
    product_list = product_list.distinct()

    # فیلتر بر اساس محصولات جدید (بر اساس تاریخ ایجاد)
    sort_filter = request.GET.get('sort')
    if sort_filter == 'newest':
        product_list = product_list.order_by('-created_at')  # فرض بر اینکه محصول تاریخ ایجاد دارد
    elif sort_filter == 'most_viewed':
        product_list = product_list.order_by('-views')  # محصولات پر بازدید

    # صفحه‌بندی
    paginator = Paginator(product_list, 6)  # 6 محصول در هر صفحه
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # اضافه کردن اطلاعات آخرین مدرس به هر محصول
    for product in page_obj:
        last_instructor = product.instructors.last() if product.instructors.exists() else None
        product.last_instructor = last_instructor

    # بازگشت به قالب با اطلاعات صفحه‌بندی و محصولات
    return render(request, 'product_list.html', {
        'page_obj': page_obj,  # اطلاعات صفحه‌بندی
        'products': page_obj.object_list,  # لیست محصولات
        'search_query': search_query,  # ذخیره عبارت جستجو برای نمایش در فرم
    })


# View برای نمایش جزئیات محصول
def product_detail(request, product_id):
    # گرفتن محصول مورد نظر بر اساس id
    product = get_object_or_404(Product, id=product_id)

    # بررسی ثبت‌نام کاربر در دوره
    is_enrolled = False
    if request.user.is_authenticated:
        is_enrolled = Enrollment.objects.filter(user=request.user, product=product).exists()

    # اطلاعات لازم برای نمایش در قالب
    context = {
        'product': product,
        'is_enrolled': is_enrolled,
        'instructors': product.instructors.all(),  # مدرسین دوره
        'features_primary': product.features_primary.all(),  # ویژگی‌های اصلی دوره
        'features_additional': product.features_additional.all(),  # ویژگی‌های اضافی دوره
    }

    return render(request, 'course/product_detail.html', context)


def category_list(request):
    categories = Category.objects.all()
    return render(request, 'Category.html', {'categories': categories})



def category_detail(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = category.products.all()  # دسترسی به محصولات این دسته‌بندی
    return render(request, 'product_list.html', {'category': category, 'products': products})


def product_detail(request, product_id):
    # گرفتن محصول مورد نظر بر اساس id
    product = get_object_or_404(Product, id=product_id)
    product.views = (product.views or 0) + 1
    product.save()

    # بررسی ثبت‌نام کاربر در دوره
    is_enrolled = False
    if request.user.is_authenticated:
        is_enrolled = Enrollment.objects.filter(user=request.user, product=product).exists()

    context = {
        'product': product,
        'is_enrolled': is_enrolled,
        'instructors': product.instructors.all(),
        'features_primary': product.features_primary.all(),
        'features_additional': product.features_additional.all(),
    }

    return render(request, 'product_detail.html', context)


def video_detail(request, video_id):
    video = get_object_or_404(Video, id=video_id)

    return render(request, 'course/video_detail.html', {'video': video})



def enroll_in_course(request, product_id):
    # logic for enrolling the user in the course
    product = get_object_or_404(Product, pk=product_id)
    # ادامه روند ثبت‌نام
    return render(request, 'enroll_success.html', {'product': product})
