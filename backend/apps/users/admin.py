from django.contrib import admin
from .models import CustomersModel, TechniciansModel
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export.fields import Field



class CustomersResources(resources.ModelResource):

    class Meta:
        model = CustomersModel
        export_order = (
            'id',
            'user',
            'phone_no', 
            'created_on',
            'updated_on'
        )


class CustomersAdmin(ImportExportModelAdmin):
    model = CustomersModel
    list_display = [
        'id', 
        'user',
        'age',
        'phone_no', 
        'created_on', 
        'updated_on'
    ]
    list_filter = ['created_on', 'updated_on']
    resource_class = CustomersResources


class TechniciansResources(resources.ModelResource):

    class Meta:
        model = TechniciansModel
        export_order = (
            'id',
            'user',
            'phone_no', 
            'created_on',
            'updated_on'
        )


class TechniciansAdmin(ImportExportModelAdmin):
    list_display = ['id', 'user', 'phone_no', 'created_on', 'updated_on']
    list_filter = ['created_on', 'updated_on']
    resource_class = TechniciansResources


admin.site.register(CustomersModel, CustomersAdmin)
admin.site.register(TechniciansModel, TechniciansAdmin)
