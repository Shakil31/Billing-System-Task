from django.urls import path
from . import views

urlpatterns = [
    path('orders/', views.order_list, name='order_list'),
    path('create/', views.create_order, name='create_order'),
    path('export/', views.export_sales_csv, name='export_sales_csv'),
    path('invoice/<int:pk>/pdf/', views.generate_invoice_pdf, name='invoice_pdf'),
]
