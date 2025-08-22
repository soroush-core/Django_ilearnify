from django.shortcuts import render
from .models import Blog, Category
from django.db.models import Q


def blog_list(request):
    blogs = Blog.objects.all()
    return render(request, 'blog_list.html', {'blogs': blogs})



def blog_detail(request, blog_id):
    categories = Category.objects.all()  # گرفتن تمام دسته‌بندی‌ها
    blog = Blog.objects.get(id=blog_id)
    latest_blogs = Blog.objects.order_by('-created_at')[:5]  # Latest 5 blogs
    return render(request, 'blog_diteils.html', {
        'blog': blog,
        'latest_blogs': latest_blogs ,
        'categories': categories
    })

def category_blogs(request, category_id):
    category = Category.objects.get(id=category_id)
    blogs = Blog.objects.filter(category=category)
    return render(request, 'blog_list.html', {'category': category, 'blogs': blogs})

def all_categories(request):
    categories = Category.objects.all()
    return render(request, 'all_categories.html', {'categories': categories})



def search_blogs(request):
    query = request.GET.get('q', '')
    blogs = Blog.objects.all()

    if query:
        # جستجو بر اساس عنوان وبلاگ و یا تگ‌ها
        blogs = blogs.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(tags__name__icontains=query)  # جستجو در تگ‌ها
        ).distinct()  # برای جلوگیری از تکرار نتیجه‌ها

    return render(request, 'blog_list.html', {'blogs': blogs, 'query': query})

