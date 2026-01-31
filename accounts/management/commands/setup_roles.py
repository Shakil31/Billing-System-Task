from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from sales.models import Order
from inventory.models import Product

class Command(BaseCommand):
    help = 'Setup user roles and permissions'

    def handle(self, *args, **kwargs):
        staff_group, created = Group.objects.get_or_create(name='Staff')
        manager_group, created = Group.objects.get_or_create(name='Manager')

        # Staff Permissions
        # Can create orders, view products
        ct_order = ContentType.objects.get_for_model(Order)
        ct_product = ContentType.objects.get_for_model(Product)

        add_order = Permission.objects.get(codename='add_order', content_type=ct_order)
        view_product = Permission.objects.get(codename='view_product', content_type=ct_product)
        
        staff_group.permissions.add(add_order, view_product)

        # Manager Permissions
        # Can edit products (change price), delete orders, view profit (implicit)
        change_product = Permission.objects.get(codename='change_product', content_type=ct_product)
        delete_order = Permission.objects.get(codename='delete_order', content_type=ct_order)
        
        manager_group.permissions.add(change_product, delete_order, add_order, view_product)

        self.stdout.write(self.style.SUCCESS('Successfully setup roles: Staff, Manager'))
