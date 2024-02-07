from django.db import models


# Create your models here.
class Profile(models.Model):
    name = models.CharField(max_length=255, unique=True)
    email = models.EmailField(default='example@example.com')
    address = models.TextField(default='Null')
    mobile_number = models.CharField(max_length=15, default='0000')

