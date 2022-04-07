from django.db import models
from bank_type.models import Choose_bank
from bank_service.models import Individual, Entity
from django.conf import settings
from django.db import transaction


class Add_worker(models.Model):
    company = models.ForeignKey(
        Entity,
        on_delete=models.CASCADE,
        related_name='choose_company'
    )
    worker = models.ForeignKey(
        Individual,
        on_delete=models.CASCADE,
        related_name='choose_worker'
    )
    celery = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def __str__(self):
        return f'{self.company.entity_name}'


class Payroll_project(models.Model):
    company = models.ForeignKey(
        Add_worker,
        on_delete=models.CASCADE,
        related_name='chose_company'
    )

    def __str__(self):
        return f'Payroll project of company {self.company.entity_name}'
