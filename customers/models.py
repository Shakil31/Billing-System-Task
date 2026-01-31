from django.conf import settings
from django.db import models


class Customer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Manager / Staff")
    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=20, unique=True)
    email = models.EmailField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    def contact_info(self):
        return f"{self.name} - {self.phone}"    