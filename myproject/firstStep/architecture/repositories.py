from firstStep.models import Category, Product, Employee, Order, OrderItem

class CategoryRepository:
    def get_all(self):
        return Category.objects.all()

class ProductRepository:
    def get_all(self):
        return Product.objects.all()
        
    def get_by_id(self, product_id):
        return Product.objects.filter(id=product_id).first()

class EmployeeRepository:
    def get_suitable_employee(self, category_id):
        return Employee.objects.filter(specialization_id=category_id).first()

class OrderRepository:
    def create_order(self, client_name):
        return Order.objects.create(client_name=client_name)

    def create_order_item(self, order, product, quantity, employee):
        return OrderItem.objects.create(
            order=order, 
            product=product, 
            quantity=quantity, 
            assigned_employee=employee
        )

    def delete_order(self, order):
        order.delete()