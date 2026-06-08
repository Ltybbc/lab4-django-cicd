from django.test import TestCase
from django.urls import reverse
from .models import Category, Employee, Product, Order, OrderItem
from .architecture.repositories import OrderRepository, EmployeeRepository, ProductRepository
from .architecture.use_cases import CreateOrderUseCase, OrderCreationError

class CleanArchitectureUseCaseTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Кексы")
        self.product = Product.objects.create(name="Ванильный кекс", category=self.category)
        
        # Инициализируем наш UseCase с репозиториями
        self.use_case = CreateOrderUseCase(
            OrderRepository(), EmployeeRepository(), ProductRepository()
        )

    def test_order_fails_when_no_employee(self):
        """Проверка архитектуры: Прерывание заказа, если нет подходящего повара"""
        items_data = {self.product.id: 2} # Хотим купить 2 кекса
        
        # Проверяем, что UseCase выкидывает точную ошибку
        with self.assertRaisesMessage(OrderCreationError, "Нет мастера для приготовления категории: Кексы"):
            self.use_case.execute("Анна", items_data)
        
        # Проверяем, что в базу данных ничего не записалось
        self.assertEqual(Order.objects.count(), 0)
        self.assertEqual(OrderItem.objects.count(), 0)