from django.contrib import admin
from .models import Product, Category, Instructor, FeaturePrimary, FeatureAdditional, Video, CourseContent

# کلاس Inline برای ویدیوها
class VideoInline(admin.TabularInline):
    model = Video
    extra = 1
    fields = ['title', 'link', 'content', 'product']  # اضافه کردن فیلد محصول
    show_change_link = True

# کلاس Inline برای محتوای دوره (CourseContent)
class CourseContentInline(admin.TabularInline):
    model = CourseContent
    extra = 1
    fields = ['title', 'product']  # اضافه کردن فیلد محصول
    show_change_link = True

# کلاس مدیریت محصول (Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'video_count', 'duration', 'level', 'buyers_count', 'views', 'price', 'is_free')
    search_fields = ('name', 'category__name')
    list_filter = ('level', 'category', 'is_free')
    filter_horizontal = ('instructors', 'features_primary', 'features_additional')  # فیلدهای جدید اضافه شده

    # اضافه کردن Inline برای ویدیوها و محتوای دوره
    inlines = [CourseContentInline, VideoInline]

# ثبت مدل‌ها در پنل ادمین
admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
admin.site.register(Instructor)
admin.site.register(FeaturePrimary)
admin.site.register(FeatureAdditional)
admin.site.register(Video)
admin.site.register(CourseContent)
