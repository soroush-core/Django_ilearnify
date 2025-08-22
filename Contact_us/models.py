from django.db import models

class ContactMessage(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15, blank=True, null=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True , null=True , blank=True)  # زمان ایجاد پیام

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.email}"
