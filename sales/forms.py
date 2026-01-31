from django.forms import modelformset_factory
from .models import OrderItem

OrderItemFormSet = modelformset_factory(
    OrderItem,
    fields=('product', 'quantity'),
    extra=1,
    can_delete=True
)
