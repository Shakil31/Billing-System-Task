from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=150)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    min_stock_level = models.PositiveIntegerField(default=5)
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    def is_low_stock(self):
        return self.quantity < self.min_stock_level

    def __str__(self):
        return self.name
