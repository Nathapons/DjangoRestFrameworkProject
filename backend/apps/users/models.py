from django.db import models
from django.contrib.auth.models import User
from ..framework.models import GeneralUserDetailModel, EditableModel, \
    FilterIdQuerySet
from datetime import datetime


class UserQuerySet(FilterIdQuerySet):
    def filter_user(self, user):
        return self.filter(user=user)

    def filter_first_name(self, first_name):
        return self.filter(user__first_name=first_name)

    def filter_last_name(self, last_name):
        return self.filter(user__last_name=last_name)


class CustomersModel(GeneralUserDetailModel, EditableModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer_user')
    objects = UserQuerySet.as_manager()

    @property
    def age(self):
        # Create age fields and apply in django admin
        birthday_year = self.birth_date.year
        now = datetime.now().year
        if birthday_year:
            return now - birthday_year
        return '-'

    def __str__(self):
        return f'[{self.id} - {self.user.get_full_name}]'
    
    class Meta:
        db_table = 'customers'
        ordering = ['-created_on']
        verbose_name = 'รายชื่อลูกค้า CustomersModel'
        verbose_name_plural = verbose_name


class TechniciansModel(GeneralUserDetailModel, EditableModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='technicians_user')
    objects = UserQuerySet.as_manager()

    def __str__(self):
        return f'[{self.id} - {self.user.get_full_name}]'
    
    class Meta:
        db_table = 'technicians'
        ordering = ['-created_on']
        verbose_name = 'รายชื่อพนักงาน TechniciansModel'
        verbose_name_plural = verbose_name


class SkillsQuerySet(FilterIdQuerySet):
    def filter_by_name(self, name):
        return self.filter(name=name)


class SkillsModel(EditableModel):
    name = models.CharField(max_length=255, verbose_name='ชื่อทักษะ')
    objects = SkillsQuerySet.as_manager()

    def __str__(self):
        return f'[{self.id} - {self.name}]'
    
    class Meta:
        db_table = 'skills'
        ordering = ['-created_on']
        verbose_name = 'skills_list'
        verbose_name_plural = verbose_name


class TechHasSkillQuerySet(FilterIdQuerySet):
    def filter_tech_id(self, id):
        return self.filter(technician=id)

    def filter_skill_id(self, id):
        return self.filter(skill=id)


class TechHasSkillsModel(EditableModel):
    technician = models.ForeignKey(TechniciansModel, on_delete=models.CASCADE)
    skill = models.ForeignKey(SkillsModel, on_delete=models.CASCADE)
    objects = TechHasSkillQuerySet.as_manager()

    def __str__(self):
        return f'[{self.id} - {self.technician.user.get_full_name} มีทักษะ {self.skill.name}]'

    class Meta:
        db_table = 'tech_has_skills'
        ordering = ['-created_on']
        verbose_name = 'tech_has_skills_list'
        verbose_name_plural = verbose_name
