from django.db import models
from ..users.models import SkillsModel
from ..framework.models import EditableModel, FilterIdQuerySet


class CategoryQuerySet(FilterIdQuerySet):
    def filter_by_name(self, name):
        return self.filter(name=name)

    def filter_by_category_code(self, category_code):
        return self.filter(catergory_code=category_code)


class CategoryModel(EditableModel):
    name = models.CharField(max_length=255, verbose_name='ชิ่อหมวดหมู่')
    category_code = models.CharField(max_length=3, verbose_name='รหัสหมวดหมู่')
    objects = CategoryQuerySet.as_manager()

    def __str__(self):
        return f'[{self.id} - {self.name}]'

    class Meta:
        db_table = 'category'
        ordering = ['-created_on']
        verbose_name = 'หมวดหมู่สินค้า CategoryModel'
        verbose_name_plural = verbose_name


class ServiceQuerySet(FilterIdQuerySet):
    def filter_by_name(self, name):
        return self.filter(name=name)

    def filter_by_category(self, category_id):
        return self.filter(category=category_id)


class ServiceModel(EditableModel):
    category = models.ForeignKey(
        CategoryModel, 
        on_delete=models.CASCADE, 
        related_name='service_category'
    )
    name = models.CharField(max_length=255, verbose_name='ชื่อ service')
    price = models.DecimalField(max_digits=99, decimal_places=2, verbose_name='ราคา')
    objects = ServiceQuerySet.as_manager()

    def __str__(self):
        return f'[{self.id} - {self.name}]'

    class Meta:
        db_table = 'service'
        ordering = ['-created_on']
        verbose_name = 'รายการบริการ ServiceModel'
        verbose_name_plural = verbose_name


class ServiceRequireSkillQuerySet(FilterIdQuerySet):
    def filter_by_service(self, id):
        return self.filter(service=id)

    def filter_by_skill(self, id):
        return self.filter(skill=id)


class ServiceRequireSkillModel(models.Model):
    service = models.ForeignKey(
        ServiceModel, 
        on_delete=models.CASCADE
    )
    skill = models.ForeignKey(
        SkillsModel, 
        on_delete=models.CASCADE
    )
    objects = ServiceRequireSkillQuerySet.as_manager()

    class Meta:
        db_table = 'service_require_skill'
        verbose_name = 'รายชื่อทักษะที่ใช้ในการบริการ ServiceRequireSkillModel'
        verbose_name_plural = verbose_name
