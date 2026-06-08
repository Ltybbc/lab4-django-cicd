from rest_framework import serializers
from .models import Category, Employee, Product, Order, OrderItem

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class EmployeeSerializer(serializers.ModelSerializer):
    specialization_name = serializers.StringRelatedField(source='specialization', read_only=True)
    class Meta:
        model = Employee
        fields = ['id', 'name', 'specialization', 'specialization_name']

class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.StringRelatedField(source='category', read_only=True)
    class Meta:
        model = Product
        fields = ['id', 'name', 'category', 'category_name']

class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.StringRelatedField(source='product', read_only=True)
    employee_name = serializers.StringRelatedField(source='assigned_employee', read_only=True)
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name', 'quantity', 'assigned_employee', 'employee_name']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    class Meta:
        model = Order
        fields = ['id', 'client_name', 'created_at', 'items']