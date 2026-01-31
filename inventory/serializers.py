from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    is_low_stock = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'purchase_price', 'selling_price', 'quantity', 'min_stock_level', 'is_active', 'is_low_stock']

    def get_is_low_stock(self, obj):
        return obj.is_low_stock()
