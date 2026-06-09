from firstStep.models import Category, Product, Employee, Order, OrderItem

class CategoryRepository:
    def get_all(self): return Category.objects.all()
    def get_by_id(self, cat_id): return Category.objects.filter(id=cat_id).first()
    def create(self, name): return Category.objects.create(name=name)
    def update(self, category, name):
        category.name = name
        category.save()
        return category
    def delete(self, category): category.delete()

class ProductRepository:
    def get_all(self): return Product.objects.all()
    def get_by_id(self, prod_id): return Product.objects.filter(id=prod_id).first()
    def create(self, name, category): return Product.objects.create(name=name, category=category)
    def update(self, product, name, category):
        product.name = name
        product.category = category
        product.save()
        return product
    def delete(self, product): product.delete()

class EmployeeRepository:
    def get_all(self): return Employee.objects.all()
    def get_by_id(self, emp_id): return Employee.objects.filter(id=emp_id).first()
    def create(self, name, specialization): return Employee.objects.create(name=name, specialization=specialization)
    def update(self, employee, name, specialization):
        employee.name = name
        employee.specialization = specialization
        employee.save()
        return employee
    def delete(self, employee): employee.delete()
    def get_suitable_employee(self, category_id):
        # Ищет первого доступного сотрудника по его специализации
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