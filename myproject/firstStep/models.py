from django.db import models

class Category(models.Model):
    name = models.CharField("Категория", max_length=100)

    def __str__(self):
        return self.name

class Employee(models.Model):
    name = models.CharField("Имя сотрудника", max_length=100)
    specialization = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Специализация")

    def __str__(self):
        return f"{self.name} ({self.specialization.name})"

class Product(models.Model):
    name = models.CharField("Название продукта", max_length=150)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория")
    
    def __str__(self):
        return self.name

class Order(models.Model):
    client_name = models.CharField("Имя клиента", max_length=100)
    created_at = models.DateTimeField("Время заказа", auto_now_add=True)

    def __str__(self):
        return f"Заказ #{self.id} от {self.client_name}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name="Заказ")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Продукт")
    quantity = models.PositiveIntegerField("Количество (шт.)")
    assigned_employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Назначенный сотрудник")

    def __str__(self):
        return f"{self.product.name} ({self.quantity} шт.)"