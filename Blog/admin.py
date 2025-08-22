# admin.py

from django.contrib import admin
from .models import Blog, Category, Author, Tag


class BlogAdmin(admin.ModelAdmin):
    # نمایش فیلدهای مورد نظر در صفحه لیست وبلاگ‌ها
    list_display = ('title', 'category', 'view_count', 'get_authors', 'created_at', 'get_tags')
    list_filter = ('category', 'tags')  # فیلتر بر اساس دسته‌بندی و تگ‌ها
    search_fields = ('title', 'description')  # جستجو بر اساس عنوان و توضیحات
    date_hierarchy = 'created_at'  # نمایش دسته‌بندی بر اساس تاریخ

    # نمایش نویسندگان وبلاگ‌ها
    def get_authors(self, obj):
        return ", ".join([author.name for author in obj.authors.all()])

    get_authors.short_description = 'نویسندگان'

    # نمایش تگ‌های وبلاگ‌ها
    def get_tags(self, obj):
        return ", ".join([tag.name for tag in obj.tags.all()])

    get_tags.short_description = 'تگ‌ها'

    # برای نمایش تصویر وبلاگ در لیست
    def image_tag(self, obj):
        return obj.image.url if obj.image else 'بدون تصویر'

    image_tag.short_description = 'تصویر'

    # نمایش تاریخ ایجاد وبلاگ‌ها به فرمت مورد نظر
    def created_at_display(self, obj):
        return obj.created_at.strftime('%Y/%m/%d')

    created_at_display.short_description = 'تاریخ ایجاد'

    # اضافه کردن فیلدهای متنی به فرم ویرایش
    fieldsets = (
        (None, {
            'fields': ('title', 'image', 'category', 'description', 'authors', 'tags')
        }),
        ('تاریخ‌ها', {
            'fields': ('created_at', 'updated_at')
        }),
    )

    readonly_fields = ('created_at', 'updated_at')  # تاریخ‌ها غیرقابل ویرایش


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'bio', 'image_tag')
    search_fields = ('name',)

    def image_tag(self, obj):
        return obj.image.url if obj.image else 'بدون تصویر'

    image_tag.short_description = 'تصویر'


class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


# ثبت مدل‌ها در پنل ادمین
admin.site.register(Blog, BlogAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Tag, TagAdmin)
