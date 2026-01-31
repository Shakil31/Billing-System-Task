from rest_framework import viewsets, permissions
from rest_framework.response import Response
from django.db.models import Sum, F
from django.utils import timezone
from sales.models import Order, OrderItem
# PDF Imports
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
import rest_framework

class DashboardViewSet(viewsets.ViewSet):
    """
    API endpoint that returns sales metrics.
    """
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        today = timezone.now().date()
        
        total_sales = Order.objects.filter(
            created_at__date=today,
            is_paid=True
        ).aggregate(Sum('total_amount'))['total_amount__sum'] or 0

        pending = Order.objects.filter(is_paid=False).count()

        # Manager Only
        is_manager = request.user.groups.filter(name='Manager').exists() or request.user.is_superuser
        profit = 0
        if is_manager:
            profit = OrderItem.objects.filter(
                order__created_at__date=today,
                order__is_paid=True
            ).aggregate(
                profit=Sum((F('price') - F('product__purchase_price')) * F('quantity'))
            )['profit'] or 0
        return Response({
            'sales': total_sales,
            'pending': pending,
            'profit': profit if is_manager else None,
            'is_manager': is_manager
        })

    @rest_framework.decorators.action(detail=False, methods=['get'])
    def export_summary_csv(self, request):
        today = timezone.now().date()
        import csv
        
        # Calculate metrics
        total_sales = Order.objects.filter(
            created_at__date=today,
            is_paid=True
        ).aggregate(Sum('total_amount'))['total_amount__sum'] or 0

        pending = Order.objects.filter(is_paid=False).count()

        is_manager = request.user.groups.filter(name='Manager').exists() or request.user.is_superuser
        profit = 0
        if is_manager:
            profit = OrderItem.objects.filter(
                order__created_at__date=today,
                order__is_paid=True
            ).aggregate(
                profit=Sum((F('price') - F('product__purchase_price')) * F('quantity'))
            )['profit'] or 0

        # Generate CSV Response
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="daily_summary_{today}.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Date', 'Total Sales', 'Pending Orders', 'Total Profit (Manager Only)'])
        writer.writerow([today, total_sales, pending, profit if is_manager else 'N/A'])
        
        return response

    @rest_framework.decorators.action(detail=False, methods=['get'])
    def export_purchase_summary(self, request):
        """
        Exports a summary of inventory purchase value (Cost of Goods).
        """
        from inventory.models import Product
        import csv
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="inventory_purchase_summary.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Product Name', 'Current Quantity', 'Purchase Price', 'Total Purchase Value'])
        
        products = Product.objects.filter(is_active=True)
        total_value = 0
        
        for p in products:
            value = p.quantity * p.purchase_price
            total_value += value
            writer.writerow([p.name, p.quantity, p.purchase_price, value])
            
        writer.writerow([])
        writer.writerow(['TOTAL INVENTORY VALUE', '', '', total_value])
        
        return response
