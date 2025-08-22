from django.db import models
from django.contrib.auth.models import User
from Blog.models import Tag


# مدل دسته‌بندی محصول
class Category(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True, help_text="نام دسته‌بندی محصول را وارد کنید.")
    description = models.TextField(null=True, blank=True)
    icon = models.ImageField(upload_to='category_icons/', null=True, blank=True)

    def __str__(self):
        return self.name


# مدل مدرس
class Instructor(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True, help_text="نام مدرس را وارد کنید.")
    image = models.ImageField(upload_to='instructors/', blank=True, null=True, help_text="تصویر مدرس را بارگذاری کنید.")
    description = models.TextField(blank=True, null=True, help_text="توضیحات مربوط به مدرس را وارد کنید.")

    def __str__(self):
        return self.name


# مدل ویژگی‌های اصلی محصول
class FeaturePrimary(models.Model):
    name = models.CharField(max_length=255, help_text="نام ویژگی اصلی محصول را وارد کنید.")

    def __str__(self):
        return self.name


# مدل ویژگی‌های اضافی محصول
class FeatureAdditional(models.Model):
    name = models.CharField(max_length=255, help_text="نام ویژگی اضافی محصول را وارد کنید.")

    def __str__(self):
        return self.name


# مدل محصول (دوره)
class Product(models.Model):
    LEVEL_CHOICES = [
        ('beginner', 'مبتدی'),
        ('intermediate', 'متوسط'),
        ('advanced', 'پیشرفته'),
    ]

    name = models.CharField(max_length=255, blank=True, null=True, help_text="نام محصول را وارد کنید.")
    image = models.ImageField(upload_to='products/', blank=True, null=True, help_text="تصویر محصول را بارگذاری کنید.")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True,
                                 related_name='products', help_text="دسته‌بندی محصول را انتخاب کنید.")
    video_count = models.IntegerField(blank=True, null=True, help_text="تعداد ویدیوهای دوره را وارد کنید.")
    duration = models.DurationField(blank=True, null=True, help_text="مدت زمان دوره را وارد کنید.")
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, blank=True, null=True,
                             help_text="سطح محصول (مبتدی، متوسط، پیشرفته) را انتخاب کنید.")
    description = models.TextField(blank=True, null=True, help_text="توضیحات محصول را وارد کنید.")
    description_secondary = models.TextField(blank=True, null=True, help_text="توضیحات تکمیلی محصول را وارد کنید.")
    views = models.IntegerField(default=0, blank=True, null=True, help_text="تعداد بازدیدهای محصول.")
    buyers_count = models.IntegerField(default=0, blank=True, null=True, help_text="تعداد خریداران محصول.")
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True,
                                help_text="قیمت محصول را وارد کنید.")
    is_free = models.BooleanField(default=False, blank=True, null=True, help_text="آیا محصول رایگان است؟")
    has_certificate = models.BooleanField(default=False, blank=True, null=True, help_text="آیا این محصول مدرک می‌دهد؟")
    instructors = models.ManyToManyField(Instructor, related_name="products", blank=True,
                                         help_text="مدرسین این محصول را انتخاب کنید.")
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True, help_text="تاریخ ایجاد محصول.")

    features_primary = models.ManyToManyField(FeaturePrimary, blank=True, related_name='products',
                                              help_text="ویژگی‌های اصلی محصول را انتخاب کنید.")
    features_additional = models.ManyToManyField(FeatureAdditional, blank=True, related_name='products',
                                                 help_text="ویژگی‌های اضافی محصول را انتخاب کنید.")
    tags = models.ManyToManyField(Tag, related_name='products', blank=True )

    def __str__(self):
        return self.name


# مدل محتوای دوره
class CourseContent(models.Model):
    title = models.CharField(max_length=255, help_text="عنوان سر فصل دوره را وارد کنید.")
    product = models.ForeignKey(Product, related_name='course_contents', on_delete=models.CASCADE, help_text="دوره مرتبط را انتخاب کنید.")

    def __str__(self):
        return self.title


# مدل ویدیوها
class Video(models.Model):
    title = models.CharField(blank=True , null=True ,max_length=255, help_text="عنوان ویدیو را وارد کنید.")
    link = models.URLField( blank=True , null=True , help_text="لینک ویدیو را وارد کنید.")
    content = models.ForeignKey( 'CourseContent', related_name='videos', on_delete=models.CASCADE, help_text="سر فصل مرتبط با ویدیو را انتخاب کنید." , blank=True , null=True ,)
    product = models.ForeignKey('Product', related_name='videos', on_delete=models.CASCADE, help_text="محصول (دوره) مرتبط با ویدیو را انتخاب کنید." , blank=True , null=True )  # اضافه کردن ForeignKey به محصول (دوره)

    def __str__(self):
        return self.title


# مدل ثبت‌نام در دوره
class Enrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='enrollments')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} enrolled in {self.product.name}"



