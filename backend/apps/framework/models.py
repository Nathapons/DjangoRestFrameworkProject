from django.db import models
from django.contrib.auth import get_user_model
import datetime


User = get_user_model()


class FilterIdQuerySet(models.QuerySet):
    def filter_id(self, id):
        return self.filter(id=id)


class EditableModel(models.Model):
    created_on = models.DateTimeField(auto_now_add=True, verbose_name='สร้างวันที่')
    updated_on = models.DateTimeField(auto_now=True, verbose_name='อัพเดตวันที่')

    class Meta:
        abstract = True


class GeneralUserDetailModel(models.Model):
    phone_no = models.CharField(max_length=20, default='-', null=True, verbose_name='เบอร์โทรติดต่อ')
    birth_date = models.DateField(null=True, blank=True, verbose_name='วันเกิด')
    country = models.CharField(max_length=100, verbose_name='ประเทศที่อยู่', default='Thai')
    address = models.TextField(verbose_name='ที่อยู่อาศัยปัจจุบัน', default='Bangkok')
    
    class Meta:
        abstract = True