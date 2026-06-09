from django.urls import path, include
from rest_framework.routers import DefaultRouter

# Вот здесь импорты с точкой сработают, потому что views.py лежит рядом!
from . import views
from . import api_views 

# Настраиваем роутер для API
router = DefaultRouter()
router.register(r'categories', api_views.CategoryViewSet)
router.register(r'employees', api_views.EmployeeViewSet)
router.register(r'products', api_views.ProductViewSet)
router.register(r'orders', api_views.OrderViewSet)

urlpatterns = [
    # Клиентская часть
    path('', views.create_order, name='create_order'),
    path('success/', views.success_view, name='success_url'),
    
    # API
    path('api/', include(router.urls)),
    
    # Панель администратора
    path('custom-admin', views.CustomAdminDashboard.as_view(), name='custom_admin_dashboard'),

    path('custom-admin/products/create/', views.ProductCRUDView.as_view(), name='custom_admin_product_create'),
    path('custom-admin/products/<int:pk>/update/', views.ProductCRUDView.as_view(), name='custom_admin_product_update'),
    path('custom-admin/products/<int:pk>/delete/', views.ProductDeleteView.as_view(), name='custom_admin_product_delete'),

    path('custom-admin/categories/create/', views.CategoryCRUDView.as_view(), name='custom_admin_category_create'),
    path('custom-admin/categories/<int:pk>/update/', views.CategoryCRUDView.as_view(), name='custom_admin_category_update'),
    path('custom-admin/categories/<int:pk>/delete/', views.CategoryDeleteView.as_view(), name='custom_admin_category_delete'),

    path('custom-admin/employees/create/', views.EmployeeCRUDView.as_view(), name='custom_admin_employee_create'),
    path('custom-admin/employees/<int:pk>/update/', views.EmployeeCRUDView.as_view(), name='custom_admin_employee_update'),
    path('custom-admin/employees/<int:pk>/delete/', views.EmployeeDeleteView.as_view(), name='custom_admin_employee_delete'),
]