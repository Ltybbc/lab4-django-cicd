from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views import View
# Импорты чистой архитектуры
from .architecture.repositories import CategoryRepository, ProductRepository, OrderRepository, EmployeeRepository
from .architecture.use_cases import CreateOrderUseCase, OrderCreationError, CategoryUseCases, ProductUseCases, EmployeeUseCases, DomainCRUDError


# ==========================================
# ЧАСТЬ 1: КЛИЕНТСКИЙ ИНТЕРФЕЙС (ИСПОЛЬЗУЕТ USE CASES)
# ==========================================

def create_order(request):
    cat_repo = CategoryRepository()
    prod_repo = ProductRepository()
    
    categories = cat_repo.get_all()
    products = prod_repo.get_all()

    if request.method == 'POST':
        client_name = request.POST.get('client_name', '').strip()
        
        # Собираем данные в словарь {id_продукта: количество}
        items_data = {}
        for product in products:
            quantity_str = request.POST.get(f'quantity_{product.id}')
            if quantity_str and quantity_str.isdigit() and int(quantity_str) > 0:
                items_data[product.id] = int(quantity_str)

        # Инициализируем UseCase нужными репозиториями
        use_case = CreateOrderUseCase(
            order_repo=OrderRepository(),
            employee_repo=EmployeeRepository(),
            product_repo=prod_repo
        )

        try:
            # Делегируем всю бизнес-логику в Use Case
            use_case.execute(client_name=client_name, items_data=items_data)
            return redirect('success_url')
        except OrderCreationError as error_msg:
            # Если логика выкинула ошибку, ловим её и показываем юзеру
            return render(request, 'product/index.html', {'categories': categories, 'error': str(error_msg)})

    return render(request, 'product/index.html', {'categories': categories})

def success_view(request):
    return render(request, 'product/success.html')


# ==========================================
# ЧАСТЬ 2: КАСТОМНАЯ ПАНЕЛЬ АДМИНИСТРАТОРА (CRUD)
# ==========================================

class SuperUserRequiredMixin(UserPassesTestMixin):
    login_url = '/admin/login/' 
    def test_func(self):
        return self.request.user.is_superuser

# ==========================================
# DASHBOARD (Отображение всего)
# ==========================================
class CustomAdminDashboard(SuperUserRequiredMixin, View):
    def get(self, request):
        context = {
            'categories': CategoryRepository().get_all(),
            'products': ProductRepository().get_all(),
            'employees': EmployeeRepository().get_all()
        }
        return render(request, 'product/admin_dashboard.html', context)


# --- КАТЕГОРИИ ---
class CategoryCRUDView(SuperUserRequiredMixin, View):
    def get(self, request, pk=None):
        context = {}
        if pk: context['category'] = CategoryRepository().get_by_id(pk)
        return render(request, 'product/admin_category_form.html', context)

    def post(self, request, pk=None):
        name = request.POST.get('name', '')
        use_cases = CategoryUseCases(CategoryRepository())
        try:
            if pk: use_cases.update(pk, name)
            else: use_cases.create(name)
            return redirect('custom_admin_dashboard')
        except DomainCRUDError as e:
            context = {'error': str(e), 'category': CategoryRepository().get_by_id(pk) if pk else None}
            return render(request, 'product/admin_category_form.html', context)

class CategoryDeleteView(SuperUserRequiredMixin, View):
    def get(self, request, pk):
        # GET-запрос: показываем страницу подтверждения
        category = CategoryRepository().get_by_id(pk)
        return render(request, 'product/admin_category_confirm_delete.html', {'category': category})

    def post(self, request, pk):
        # POST-запрос: физически удаляем
        CategoryUseCases(CategoryRepository()).delete(pk)
        return redirect('custom_admin_dashboard')

# --- ПРОДУКТЫ ---
class ProductCRUDView(SuperUserRequiredMixin, View):
    def get(self, request, pk=None):
        context = {'categories': CategoryRepository().get_all()}
        if pk: context['product'] = ProductRepository().get_by_id(pk)
        return render(request, 'product/admin_product_form.html', context)

    def post(self, request, pk=None):
        name = request.POST.get('name', '')
        category_id = int(request.POST.get('category_id', 0) or 0)
        use_cases = ProductUseCases(ProductRepository(), CategoryRepository())
        try:
            if pk: use_cases.update(pk, name, category_id)
            else: use_cases.create(name, category_id)
            return redirect('custom_admin_dashboard')
        except DomainCRUDError as e:
            context = {
                'error': str(e), 
                'categories': CategoryRepository().get_all(),
                'product': ProductRepository().get_by_id(pk) if pk else None
            }
            return render(request, 'product/admin_product_form.html', context)

class ProductDeleteView(SuperUserRequiredMixin, View):
    def get(self, request, pk):
        product = ProductRepository().get_by_id(pk)
        return render(request, 'product/admin_product_confirm_delete.html', {'product': product})

    def post(self, request, pk):
        ProductUseCases(ProductRepository(), CategoryRepository()).delete(pk)
        return redirect('custom_admin_dashboard')

# --- СОТРУДНИКИ ---
class EmployeeCRUDView(SuperUserRequiredMixin, View):
    def get(self, request, pk=None):
        context = {'categories': CategoryRepository().get_all()}
        if pk: context['employee'] = EmployeeRepository().get_by_id(pk)
        return render(request, 'product/admin_employee_form.html', context)

    def post(self, request, pk=None):
        name = request.POST.get('name', '')
        specialization_id = int(request.POST.get('specialization_id', 0) or 0)
        use_cases = EmployeeUseCases(EmployeeRepository(), CategoryRepository())
        try:
            if pk: use_cases.update(pk, name, specialization_id)
            else: use_cases.create(name, specialization_id)
            return redirect('custom_admin_dashboard')
        except DomainCRUDError as e:
            context = {
                'error': str(e), 
                'categories': CategoryRepository().get_all(),
                'employee': EmployeeRepository().get_by_id(pk) if pk else None
            }
            return render(request, 'product/admin_employee_form.html', context)

class EmployeeDeleteView(SuperUserRequiredMixin, View):
    def get(self, request, pk):
        employee = EmployeeRepository().get_by_id(pk)
        return render(request, 'product/admin_employee_confirm_delete.html', {'employee': employee})

    def post(self, request, pk):
        EmployeeUseCases(EmployeeRepository(), CategoryRepository()).delete(pk)
        return redirect('custom_admin_dashboard')