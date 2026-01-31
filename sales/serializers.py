from rest_framework import serializers
from django.db import transaction
from django.db.models import F
from .models import Order, OrderItem
from inventory.models import Product
from customers.models import Customer

class OrderItemSerializer(serializers.ModelSerializer):
    price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    product_name = serializers.ReadOnlyField(source='product.name')

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name', 'quantity', 'price', 'line_total']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, required=False)
    customer_name = serializers.ReadOnlyField(source='customer.name')
    # Customer is optional for input, handled in view
    customer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all(), required=False)

    # Simplified fields for HTML Form (Browsable API)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.filter(is_active=True), 
        write_only=True, 
        required=False,
        source='simple_product'
    )
    quantity = serializers.IntegerField(write_only=True, required=False, min_value=1, default=1)

    class Meta:
        model = Order
        fields = ['id', 'product_id', 'quantity', 'customer', 'customer_name', 'is_paid', 'total_amount', 'created_at', 'items']

        read_only_fields = ['invoice_number', 'total_amount', 'created_at']

    def validate(self, attrs):
        # Ensure either 'items' list OR ('product_id' + 'quantity') is present
        if not attrs.get('items') and not attrs.get('simple_product'):
            raise serializers.ValidationError("Please provide either a list of 'items' (JSON) or a 'product_id' and 'quantity' (HTML Form).")
        return attrs

    def create(self, validated_data):
        items_data = validated_data.pop('items', [])
        simple_product = validated_data.pop('simple_product', None)
        quantity = validated_data.pop('quantity', 1)

        # If simple form is used, convert to item list structure
        if simple_product:
            items_data.append({
                'product': simple_product,
                'quantity': quantity
            })
            
        with transaction.atomic():
            order = Order.objects.create(**validated_data)
            total = 0
            
            for item_data in items_data:
                # Lock the product row to prevent race conditions
                product = Product.objects.select_for_update().get(pk=item_data['product'].pk)
                qty = item_data['quantity']

                # Stock Check
                if product.quantity < qty:
                    raise serializers.ValidationError(f"Not enough stock for {product.name}. Available: {product.quantity}")

                # Atomic Decrement
                product.quantity = product.quantity - qty
                product.save()
                
                # Fetch fresh price
                price = product.selling_price
                
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=qty,
                    price=price
                )
                
                total += price * qty
            
            order.total_amount = total
            order.save()
            
        return order
