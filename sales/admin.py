from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['line_total']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['invoice_number', 'customer', 'total_amount', 'is_paid', 'created_at']
    list_filter = ['is_paid', 'created_at']
    search_fields = ['invoice_number', 'customer__name']
    inlines = [OrderItemInline]
    readonly_fields = ['invoice_number', 'created_at']
