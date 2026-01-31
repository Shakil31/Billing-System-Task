from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from inventory.views import ProductViewSet
from sales.views import OrderViewSet
from dashboard.views import DashboardViewSet
from customers.views import CustomerViewSet
from accounts.views import LoginView, logout_view, RegistrationView

# API Router
router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'orders', OrderViewSet, basename='order')

router.register(r'dashboard', DashboardViewSet, basename='dashboard')
router.register(r'customers', CustomerViewSet, basename='customer')

urlpatterns = [
    path('admin/', admin.site.urls),
    # API Routes
    path('api/', include(router.urls)),
    # Browsable API login
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
     
    # Dashboard API (kept here or moved to router)
    # path('api/dashboard/', DashboardView.as_view(), name='api_dashboard'), 
    # Refactoring dashboard to ViewSet below, so commenting out or removing.
    
    # Auth
    path('accounts/login/', LoginView.as_view(), name='login'),
    path('accounts/logout/', logout_view, name='logout'),
    
    # We can keep or remove old include paths. 
    # For clarity, let's just keep API and Admin as requested "without html".
]
