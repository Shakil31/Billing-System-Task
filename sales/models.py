from django.db import models
from django.utils import timezone
from customers.models import Customer
from inventory.models import Product

class Order(models.Model):
    invoice_number = models.CharField(max_length=20, unique=True, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    is_paid = models.BooleanField(default=False)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new and not self.invoice_number:
            self.invoice_number = f"INV-{timezone.now().year}-{self.pk:04d}"
            Order.objects.filter(pk=self.pk).update(invoice_number=self.invoice_number)
    def __str__(self):
        return self.invoice_number
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    def line_total(self):
        return self.quantity * self.price