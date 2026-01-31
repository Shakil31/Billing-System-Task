from rest_framework import viewsets, permissions
from .models import Customer
from .serializers import CustomerSerializer

class CustomerViewSet(viewsets.ModelViewSet):
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAdminUser]
    search_fields = ['name', 'phone', 'email']
    queryset = Customer.objects.filter(is_active=True).order_by('name')
