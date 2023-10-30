from django.contrib import admin
from .models import ServiceProduct

@admin.register(ServiceProduct)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'available', 'category', )
    list_filter = ('available', 'category')
    search_fields = ('name', 'category')
    ordering = ('name',)
