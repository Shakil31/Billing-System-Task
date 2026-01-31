from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from inventory.models import Product
from sales.models import Order
from .models import AuditLog
from .middleware import get_current_user
import json
from django.core.serializers.json import DjangoJSONEncoder

@receiver(pre_save, sender=Product)
def track_product_changes(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_instance = Product.objects.get(pk=instance.pk)
            instance._old_instance = old_instance
        except Product.DoesNotExist:
            instance._old_instance = None

@receiver(post_save, sender=Product)
def log_product_changes(sender, instance, created, **kwargs):
    user = get_current_user()
    details = {}
    
    if created:
        action = 'CREATE'
        details = {'name': instance.name, 'quantity': instance.quantity, 'price': str(instance.selling_price)}
    else:
        action = 'UPDATE'
        old = getattr(instance, '_old_instance', None)
        if old:
            if old.quantity != instance.quantity:
                details['quantity_change'] = {'from': old.quantity, 'to': instance.quantity}
            if old.selling_price != instance.selling_price:
                details['price_change'] = {'from': str(old.selling_price), 'to': str(instance.selling_price)}
            
            # If no changes in relevant fields, maybe don't log? 
            # But let's log if details exist.
    
    if details or action == 'CREATE':
        AuditLog.objects.create(
            action=action,
            model_name='Product',
            object_id=instance.pk,
            user=user if user and user.is_authenticated else None,
            details=json.loads(json.dumps(details, cls=DjangoJSONEncoder))
        )

@receiver(post_save, sender=Order)
def log_order_creation(sender, instance, created, **kwargs):
    if created:
        user = get_current_user()
        AuditLog.objects.create(
            action='CREATE',
            model_name='Order',
            object_id=instance.pk,
            user=user if user and user.is_authenticated else None,
            details={'invoice_number': instance.invoice_number, 'total': str(instance.total_amount)}
        )
