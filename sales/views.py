from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
import csv
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderItemSerializer

from .filters import OrderFilter
from customers.models import Customer
from django.db.models import F
from django_filters.rest_framework import DjangoFilterBackend

from core.permissions import IsManager, IsStaff

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_class = OrderFilter
    search_fields = ['customer__name', 'customer__phone', 'invoice_number']

    def get_permissions(self):
        if self.action in ['destroy', 'update', 'partial_update']:
            return [IsManager()]
        # Create, List, Retrieve allow Staff
        return [IsStaff()]

    def get_queryset(self):
        # Only Staff/Admins can access this view now
        return Order.objects.select_related('customer').order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save()


    @action(detail=True, methods=['get'])
    def pdf(self, request, pk=None):
        order = self.get_object()
        template_path = 'sales/invoice_pdf.html'
        context = {'order': order}
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="invoice_{order.invoice_number}.pdf"'
        
        template = get_template(template_path)
        html = template.render(context)
        pisa_status = pisa.CreatePDF(html, dest=response)
        
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
        return response

    @action(detail=False, methods=['get'])
    def export_csv(self, request):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="sales_report.csv"'

        writer = csv.writer(response)
        writer.writerow(['Invoice ID', 'Customer', 'Date', 'Total Amount', 'Status'])

        orders = self.filter_queryset(self.get_queryset())
        for order in orders:
            writer.writerow([
                order.invoice_number,
                order.customer.name,
                order.created_at,
                order.total_amount,
                order.is_paid
            ])
        return response

    @action(detail=False, methods=['get'])
    def export_customer_report(self, request):
        """
        Exports a summary of sales grouped by customer.
        """
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="customer_sales_report.csv"'

        writer = csv.writer(response)
        writer.writerow(['Customer Name', 'Phone', 'Total Orders', 'Total Spent'])

        from django.db.models import Count, Sum
        # Group by customer
        report = Order.objects.filter(is_paid=True).values(
            'customer__name', 'customer__phone'
        ).annotate(
            total_orders=Count('id'),
            total_spent=Sum('total_amount')
        ).order_by('-total_spent')

        for row in report:
            writer.writerow([
                row['customer__name'],
                row['customer__phone'],
                row['total_orders'],
                row['total_spent']
            ])
        return response
