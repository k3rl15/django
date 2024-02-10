from django.db import models


# Create your models here.
class Profile(models.Model):
    name = models.CharField(max_length=255, unique=True)
    email = models.EmailField(default='example@example.com')
    address = models.TextField(default='Null')
    mobile_number = models.CharField(max_length=15, default='0000')


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField(null=True, blank=True)
    category = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
