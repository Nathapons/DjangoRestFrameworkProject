from django.db import models
from ..users.models import CustomersModel, TechniciansModel
from ..services.models import ServiceModel
from ..framework.models import EditableModel, FilterIdQuerySet
import datetime


class CreditCardQueySet(FilterIdQuerySet):
    def filter_card_name(self, card_name):
        return self.filter(card_name=card_name)

    def filter_card_no(self, card_no):
        return self.filter(card_no=card_no)


class CreditCardModel(EditableModel):
    card_name = models.CharField(max_length=255, verbose_name='ชื่อบัตรเครดิต')
    card_no = models.CharField(max_length=255, verbose_name='รหัสบัตรเครดิต')
    card_expire = models.CharField(max_length=7, verbose_name='หมดอายุของบัตรเครดิต')
    objects = CreditCardQueySet.as_manager()

    def __str__(self):
        return f'[{self.id} - {self.card_name}]'

    class Meta:
        db_table = 'credit_card'
        ordering = ['-created_on']
        verbose_name = 'รายชื่อบัตรเครดิต CreditCardModel'
        verbose_name_plural = verbose_name


class OrderQuerySet(FilterIdQuerySet):
    def filter_by_customer(self, id):
        return self.filter(customer=id)

    def filter_pay_status(self, status):
        return self.filter(pay_status=status)

    def filter_work_date(self, work_date):
        if isinstance(work_date, datetime.date):
            return self.filter(work_date=work_date)
        return self.none

    def filter_location(self, location):
        return self.filter(location=location)


class OrderModel(EditableModel): 
    PAYMENT_STATUS = (
        ('COMPLETE', 'ชำระเงินเรียบร้อย'),
        ('IN_PROGRESS', 'ค้างชำระเงิน'),
        ('CANCEL', 'ยกเลิกชำระเงิน')
    )

    ORDER_STATUS = (
        ('COMPLETE', 'ดำเนินงานเสร็จสิ้น'),
        ('IN_PROGRESS', 'กำลังดำเนินงาน'),
        ('WAIT', 'รอการดำเนินงาน')
    )

    customer = models.ForeignKey(CustomersModel, on_delete=models.CASCADE)
    credit_card = models.ForeignKey(CreditCardModel, on_delete=models.CASCADE)
    pay_status = models.CharField(
        max_length=100, 
        verbose_name='สถานะการจ่ายเงิน',
        choices=PAYMENT_STATUS
    )
    work_date = models.DateField(verbose_name='วันที่ทำงาน')
    location = models.CharField(max_length=255, verbose_name='สถานที่บริการ')
    total_price = models.DecimalField(max_digits=99, decimal_places=2, verbose_name='จำนวนการคำสั่ง')
    order_status = models.CharField(max_length=100, choices=ORDER_STATUS, verbose_name='สถานะคำสั่ง')
    objects = OrderQuerySet.as_manager()

    def __str__(self):
        return f'[{self.id} - work at {self.location} on {self.work_date}]'

    class Meta:
        db_table = 'order'
        ordering = ['-created_on']
        verbose_name = 'รายการคำสั่งซื้อ OrderModel'
        verbose_name_plural = verbose_name


class OrderItemsQuerySet(FilterIdQuerySet):
    def filter_by_service(self, id):
        return self.filter(service=id)

    def filter_by_technician(self, id):
        return self.filter(technician=id)

    def filter_by_orders(self, id):
        return self.filter(orders=id)


class OrderItemsModels(EditableModel):
    service = models.ForeignKey(ServiceModel, on_delete=models.CASCADE)
    technician = models.ForeignKey(TechniciansModel, on_delete=models.CASCADE)
    orders = models.ForeignKey(OrderModel, on_delete=models.CASCADE)
    quatity = models.PositiveIntegerField(verbose_name='จำนวนการให้บริการ')
    objects = OrderItemsQuerySet.as_manager()

    def __str__(self):
        return f'[{self.id} - {self.technician.get_full_name} work {self.service.name}]'

    class Meta:
        db_table = 'order_items OrderItemsModels'
        ordering = ['-created_on']
        verbose_name = 'รายการสินค้าที่ใช้ในคำสั่งซื้อ OrderItemsModels'
        verbose_name_plural = verbose_name
