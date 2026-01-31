from rest_framework import viewsets, permissions
from .models import Product
from .serializers import ProductSerializer

from core.permissions import IsManager, IsStaff

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(is_active=True).order_by('name')
    serializer_class = ProductSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsManager()]

        return [IsStaff()]

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()
