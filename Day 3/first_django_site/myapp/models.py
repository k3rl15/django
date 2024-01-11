from django.db import models


class Profile(models.Model):
    name = models.CharField(max_length=255, unique=True)
    email = models.EmailField()
    address = models.TextField()
    mobile_number = models.CharField(max_length=15)

    def __str__(self):
        return self.name
