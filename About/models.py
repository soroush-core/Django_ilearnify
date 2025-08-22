from django.db import models


class AboutUs(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='about_us_images/')
    description = models.TextField()  # فیلد جدید برای توضیحات

    # ویژگی‌های سایت
    features = models.ManyToManyField('Feature', related_name='about_us_features')

    def __str__(self):
        return self.title


class Feature(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name




class FAQ(models.Model):
    question = models.CharField(max_length=255 , blank=True , null=True)
    answer = models.TextField(blank=True , null=True)

    def __str__(self):
        return self.question