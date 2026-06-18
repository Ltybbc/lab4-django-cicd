from .repositories import OrderRepository, EmployeeRepository, ProductRepository, CategoryRepository

class OrderCreationError(Exception):
    pass

class CreateOrderUseCase:
    def __init__(self, order_repo: OrderRepository, employee_repo: EmployeeRepository, product_repo: ProductRepository):
        self.order_repo = order_repo
        self.employee_repo = employee_repo
        self.product_repo = product_repo

    def execute(self, client_name: str, items_data: dict):
        # items_data приходит в формате {product_id: quantity}
        if not client_name:
            raise OrderCreationError("Пожалуйста, введите ваше имя.")

        valid_items = {p_id: q for p_id, q in items_data.items() if q > 0}
        
        if not valid_items:
            raise OrderCreationError("Выберите хотя бы один товар!")

        # Создаем пустую корзину
        order = self.order_repo.create_order(client_name)

        # Наполняем корзину
        for product_id, quantity in valid_items.items():
            product = self.product_repo.get_by_id(product_id)
            if not product:
                continue

            suitable_employee = self.employee_repo.get_suitable_employee(product.category_id)
            
            # ВАЛИДАЦИЯ ИЗ ОТЧЕТА: Если нет повара - отменяем заказ и прокидываем ошибку
            if not suitable_employee:
                self.order_repo.delete_order(order)
                raise OrderCreationError(f"Нет мастера для приготовления категории: {product.category.name}")

            self.order_repo.create_order_item(order, product, quantity, suitable_employee)

        return order

class DomainCRUDError(Exception):
    pass

# ==========================================
# USE CASES ДЛЯ КАТЕГОРИЙ
# ==========================================
class CategoryUseCases:
    def __init__(self, repo: CategoryRepository):
        self.repo = repo

    def create(self, name: str):
        if not name or len(name.strip()) < 3:
            raise DomainCRUDError("Название категории должно содержать минимум 3 символа.")
        return self.repo.create(name.strip())

    def update(self, cat_id: int, name: str):
        category = self.repo.get_by_id(cat_id)
        if not category: raise DomainCRUDError("Категория не найдена.")
        if not name or len(name.strip()) < 3:
            raise DomainCRUDError("Некорректное название.")
        return self.repo.update(category, name.strip())

    def delete(self, cat_id: int):
        category = self.repo.get_by_id(cat_id)
        if category: self.repo.delete(category)

# ==========================================
# USE CASES ДЛЯ ПРОДУКТОВ
# ==========================================
class ProductUseCases:
    def __init__(self, prod_repo: ProductRepository, cat_repo: CategoryRepository):
        self.prod_repo = prod_repo
        self.cat_repo = cat_repo

    def create(self, name: str, category_id: int):
        if not name.strip(): raise DomainCRUDError("Имя продукта не может быть пустым.")
        category = self.cat_repo.get_by_id(category_id)
        if not category: raise DomainCRUDError("Выбранная категория не существует.")
        return self.prod_repo.create(name.strip(), category)

    def update(self, prod_id: int, name: str, category_id: int):
        product = self.prod_repo.get_by_id(prod_id)
        if not product: raise DomainCRUDError("Продукт не найден.")
        
        category = self.cat_repo.get_by_id(category_id)
        if not category: raise DomainCRUDError("Выбранная категория не существует.")
        
        return self.prod_repo.update(product, name.strip(), category)

    def delete(self, prod_id: int):
        product = self.prod_repo.get_by_id(prod_id)
        if product: self.prod_repo.delete(product)

# ==========================================
# USE CASES ДЛЯ СОТРУДНИКОВ
# ==========================================
class EmployeeUseCases:
    def __init__(self, emp_repo: EmployeeRepository, cat_repo: CategoryRepository):
        self.emp_repo = emp_repo
        self.cat_repo = cat_repo

    def create(self, name: str, specialization_id: int):
        if not name.strip(): raise DomainCRUDError("Имя сотрудника не может быть пустым.")
        specialization = self.cat_repo.get_by_id(specialization_id)
        if not specialization: raise DomainCRUDError("Выбранная специализация не найдена.")
        return self.emp_repo.create(name.strip(), specialization)

    def update(self, emp_id: int, name: str, specialization_id: int):
        employee = self.emp_repo.get_by_id(emp_id)
        if not employee: raise DomainCRUDError("Сотрудник не найден.")
        
        specialization = self.cat_repo.get_by_id(specialization_id)
        if not specialization: raise DomainCRUDError("Выбранная специализация не найдена.")
        
        return self.emp_repo.update(employee, name.strip(), specialization)

    def delete(self, emp_id: int):
        employee = self.emp_repo.get_by_id(emp_id)
        if employee: self.emp_repo.delete(employee)