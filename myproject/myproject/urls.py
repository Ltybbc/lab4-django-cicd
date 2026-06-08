from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Перенаправляем все запросы в наше приложение
    path('', include('firstStep.urls')), 
]