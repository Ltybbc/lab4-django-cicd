from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import UserPassesTestMixin

# Импорты чистой архитектуры
from .architecture.repositories import CategoryRepository, ProductRepository, OrderRepository, EmployeeRepository
from .architecture.use_cases import CreateOrderUseCase, OrderCreationError

# Импорты моделей только для админки
from .models import Employee, Product, Order, Category

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

class CustomAdminDashboard(SuperUserRequiredMixin, TemplateView):
    template_name = 'product/admin_dashboard.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.all()
        context['categories'] = Category.objects.all()
        context['employees'] = Employee.objects.all()
        return context

# --- Products ---
class CustomAdminProductCreate(SuperUserRequiredMixin, CreateView):
    model = Product
    fields = ['name', 'category']
    template_name = 'product/admin_product_form.html'
    success_url = reverse_lazy('custom_admin_dashboard')

class CustomAdminProductUpdate(SuperUserRequiredMixin, UpdateView):
    model = Product
    fields = ['name', 'category']
    template_name = 'product/admin_product_form.html'
    success_url = reverse_lazy('custom_admin_dashboard')

class CustomAdminProductDelete(SuperUserRequiredMixin, DeleteView):
    model = Product
    template_name = 'product/admin_product_confirm_delete.html'
    success_url = reverse_lazy('custom_admin_dashboard')

# --- Categories ---
class CustomAdminCategoryCreate(SuperUserRequiredMixin, CreateView):
    model = Category
    fields = ['name']
    template_name = 'product/admin_category_form.html'
    success_url = reverse_lazy('custom_admin_dashboard')

class CustomAdminCategoryUpdate(SuperUserRequiredMixin, UpdateView):
    model = Category
    fields = ['name']
    template_name = 'product/admin_category_form.html'
    success_url = reverse_lazy('custom_admin_dashboard')

class CustomAdminCategoryDelete(SuperUserRequiredMixin, DeleteView):
    model = Category
    template_name = 'product/admin_category_confirm_delete.html'
    success_url = reverse_lazy('custom_admin_dashboard')

# --- Employees ---
class CustomAdminEmployeeCreate(SuperUserRequiredMixin, CreateView):
    model = Employee
    fields = ['name', 'specialization']
    template_name = 'product/admin_employee_form.html'
    success_url = reverse_lazy('custom_admin_dashboard')

class CustomAdminEmployeeUpdate(SuperUserRequiredMixin, UpdateView):
    model = Employee
    fields = ['name', 'specialization']
    template_name = 'product/admin_employee_form.html'
    success_url = reverse_lazy('custom_admin_dashboard')

class CustomAdminEmployeeDelete(SuperUserRequiredMixin, DeleteView):
    model = Employee
    template_name = 'product/admin_employee_confirm_delete.html'
    success_url = reverse_lazy('custom_admin_dashboard')