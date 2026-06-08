from django.contrib import admin
from .models import Category, Employee, Product, Order, OrderItem

admin.site.register(Category)
admin.site.register(Employee)
admin.site.register(Product)

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('assigned_employee',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'client_name', 'created_at')
    inlines = [OrderItemInline]