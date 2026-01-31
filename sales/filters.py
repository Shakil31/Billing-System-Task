import django_filters
from .models import Order

class OrderFilter(django_filters.FilterSet):
    start_date = django_filters.DateFilter(field_name='created_at', lookup_expr='gte', label='Start Date (YYYY-MM-DD)')
    end_date = django_filters.DateFilter(field_name='created_at', lookup_expr='lte', label='End Date (YYYY-MM-DD)')
    is_paid = django_filters.BooleanFilter(field_name='is_paid', label='Is Paid?')

    class Meta:
        model = Order
        fields = ['is_paid', 'start_date', 'end_date']
