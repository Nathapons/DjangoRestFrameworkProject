from django.contrib import admin
from .models import ServiceModel, CategoryModel


class ServiceAdmin(admin.ModelAdmin):
    list_display = ['id', 'category', 'name', 'price', 'created_on', 'updated_on']
    list_filter = ['created_on', 'updated_on']
    search_fields = ['name']

    def get_queryset(self, request):
        # increase django model performance
        qs = super().get_queryset(request).select_related('category')
        return qs


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'category_code', 'created_on', 'updated_on']
    list_filter = ['created_on', 'updated_on']
    search_fields = ['name']
    

admin.site.register(ServiceModel, ServiceAdmin)
admin.site.register(CategoryModel, CategoryAdmin)