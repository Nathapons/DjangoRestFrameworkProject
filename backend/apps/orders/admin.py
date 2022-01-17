from django.contrib import admin
from .models import CreditCardModel, OrderItemsModels, OrderModel


class CreditCardAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'card_name',
        'card_no',
        'card_expire',
        'created_on',
        'updated_on'
    ]
    list_filter = ['created_on', 'updated_on']
    search_fields = ['card_name']


class OrderItemsAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'service',
        'technician',
        'orders',
        'quatity',
        'created_on',
        'updated_on'
    ]
    list_filter = ['created_on', 'updated_on']

    def get_queryset(self, request):
        # increase django model performance
        qs = super().get_queryset(request).select_related(
            'service',
            'technician',
            'orders'
        )
        return qs


class OrderAdmin(admin.ModelAdmin):
    list_filter = ['pay_status', 'order_status', 'created_on', 'updated_on']
    list_display = [
        'id',
        'customer',
        'credit_card',
        'pay_status',
        'work_date',
        'location',
        'total_price',
        'order_status',
        'created_on',
        'updated_on'
    ]

    def get_queryset(self, request):
        # increase django model performance
        qs = super().get_queryset(request).select_related(
            'customer',
            'credit_card'
        )
        return qs


admin.site.register(CreditCardModel, CreditCardAdmin)
admin.site.register(OrderItemsModels, OrderItemsAdmin)
admin.site.register(OrderModel, OrderAdmin)
