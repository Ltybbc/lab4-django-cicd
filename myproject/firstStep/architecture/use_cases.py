from .repositories import OrderRepository, EmployeeRepository, ProductRepository

# Специальный класс для наших ошибок
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