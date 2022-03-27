import binascii
import os
from django.db import models
from django.conf import settings
from bank_type.models import Choose_bank
from django.db import transaction


class Individual(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, default='')
    bank_name = models.ForeignKey(
        Choose_bank, on_delete=models.CASCADE, default='')
    username = models.CharField(
        max_length=30, verbose_name='Full Username', null=False)
    password = models.CharField(
        max_length=9, verbose_name='Password Data', unique=True)
    id_number = models.CharField(
        max_length=14, verbose_name='Password ID', unique=True)
    user_tel = models.CharField(
        max_length=13, verbose_name='User Telephone', unique=True)
    email = models.CharField(
        max_length=35, verbose_name='User email', null=False)

    def __str__(self):
        return self.username


class Entity(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, default='')
    bank_name = models.ForeignKey(
        Choose_bank, on_delete=models.CASCADE, default='')
    first_type = 'IO'
    sec_type = 'OOO'
    third_type = 'ZAO'

    ENTITY_TYPE = (
        (first_type, 'IO'),
        (sec_type, 'OOO'),
        (third_type, 'ZAO'),
    )

    entity_type = models.CharField(
        max_length=3, verbose_name='Entity Type', choices=ENTITY_TYPE)
    entity_name = models.CharField(
        max_length=20, verbose_name='Entity Name', unique=True)
    pay_acc_number = models.CharField(
        max_length=15, verbose_name='Account Number', unique=True)
    ind_code = models.CharField(
        max_length=15, verbose_name='Identification Code', unique=True)
    address = models.CharField(
        max_length=30, verbose_name='Address', unique=True)

    def __str__(self):
        return self.entity_name


class Account(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, default=True)
    bank_acc = models.ForeignKey(
        Choose_bank, on_delete=models.CASCADE, default=True)
    balance = models.DecimalField(default=0, max_digits=12, decimal_places=2)

    def __str__(self):
        return f'{self.id} of {self.user.username}'


class Action(models.Model):
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    date = models.DateTimeField(auto_now_add=True)
    account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name='actions',
    )

    def __str__(self):
        return f'Account number {self.account.id} ' +\
            f'was changed on {str(self.amount)}'


class Transaction(models.Model):
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )
    date = models.DateTimeField(auto_now_add=True)

    account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE
    )

    merchant = models.CharField(max_length=255)

    def __str__(self):
        return f'Account number {self.account.id} ' +\
            f'sent {str(self.amount)} to {self.merchant}'

    @classmethod
    def make_transaction(cls, amount, account, merchant):
        if account.balance < amount:
            raise(ValueError('Not enough money'))

        with transaction.atomic():
            account.balance -= amount
            account.save()
            tran = cls.objects.create(
                amount=amount, account=account, merchant=merchant)

        return account, tran
