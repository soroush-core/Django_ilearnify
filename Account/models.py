# models.py
from django.db import models
from django.contrib.auth.models import User

class CustomUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    registration_date = models.DateTimeField(auto_now_add=True)  # ذخیره تاریخ ثبت‌نام
    profile_image = models.ImageField(upload_to='profile_images/', null=True,
                                      blank=True)  # فیلد جدید برای تصویر پروفایل

    def __str__(self):
        return self.user.username
