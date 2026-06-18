from django.test import TestCase
from django.urls import reverse
from .models import Category, Employee, Product, Order, OrderItem
from .architecture.repositories import OrderRepository, EmployeeRepository, ProductRepository
from .architecture.use_cases import CreateOrderUseCase, OrderCreationError

# ==========================================
# 1. ТЕСТЫ БИЗНЕС-ЛОГИКИ (USE CASES)
# ==========================================
class CleanArchitectureUseCaseTest(TestCase):
    def setUp(self):
        # Подготовка данных перед каждым тестом
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
        
        # Проверяем, что в базу данных ничего не записалось (защита от мусора)
        self.assertEqual(Order.objects.count(), 0)
        self.assertEqual(OrderItem.objects.count(), 0)

    def test_order_success(self):
        """Проверка архитектуры: Успешное создание заказа и позиций"""
        # Нанимаем сотрудника, чтобы заказ мог быть выполнен
        employee = Employee.objects.create(name="Иван", specialization=self.category)
        
        items_data = {self.product.id: 3}
        
        # Ошибки быть не должно, метод должен вернуть созданный заказ
        order = self.use_case.execute("Максим", items_data)
        
        # Проверяем, что записи появились в БД
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(OrderItem.objects.count(), 1)
        
        # Проверяем правильность сохраненных данных и автоматическое назначение сотрудника
        saved_item = OrderItem.objects.first()
        self.assertEqual(saved_item.order, order)
        self.assertEqual(saved_item.quantity, 3)
        self.assertEqual(saved_item.assigned_employee, employee)

    def test_order_fails_empty_name(self):
        """Проверка архитектуры: Ошибка при пустом имени клиента"""
        items_data = {self.product.id: 1}
        with self.assertRaisesMessage(OrderCreationError, "Пожалуйста, введите ваше имя."):
            self.use_case.execute("", items_data)
            
    def test_order_fails_empty_cart(self):
        """Проверка архитектуры: Ошибка при пустой корзине"""
        # Передаем пустой словарь товаров
        with self.assertRaisesMessage(OrderCreationError, "Выберите хотя бы один товар!"):
            self.use_case.execute("Елена", {})


# ==========================================
# 2. ТЕСТЫ БАЗЫ ДАННЫХ (MODELS)
# ==========================================
class BakeryModelTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Торты")
        self.product = Product.objects.create(name="Медовик", category=self.category)
        self.employee = Employee.objects.create(name="Ольга", specialization=self.category)

    def test_str_representations(self):
        """Проверка читаемого отображения моделей (__str__)"""
        self.assertEqual(str(self.category), "Торты")
        self.assertEqual(str(self.product), "Медовик")
        self.assertEqual(str(self.employee), "Ольга (Торты)")


# ==========================================
# 3. ТЕСТЫ КОНТРОЛЛЕРОВ (VIEWS)
# ==========================================
class BakeryViewTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Конфеты")
        self.product = Product.objects.create(name="Трюфель", category=self.category)
        self.employee = Employee.objects.create(name="Петр", specialization=self.category)
        self.create_order_url = reverse('create_order') # Ссылка на главную страницу

    def test_create_order_get(self):
        """Проверка контроллера: Открытие главной страницы (GET запрос)"""
        response = self.client.get(self.create_order_url)
        
        self.assertEqual(response.status_code, 200) # Страница работает
        self.assertTemplateUsed(response, 'product/index.html') # Используется нужный HTML
        self.assertIn('categories', response.context) # Данные меню передаются в шаблон

    def test_create_order_post_success(self):
        """Проверка контроллера: Успешная отправка формы заказа (POST запрос)"""
        # Эмулируем данные, которые отправляет HTML форма
        data = {
            'client_name': 'Дмитрий',
            f'quantity_{self.product.id}': '5'
        }
        
        response = self.client.post(self.create_order_url, data)
        
        # Проверяем, что после успеха нас перенаправило на страницу "Спасибо за заказ"
        self.assertRedirects(response, reverse('success_url'))
        
        # Убеждаемся, что контроллер дернул бизнес-логику и заказ появился в БД
        self.assertEqual(Order.objects.count(), 1)