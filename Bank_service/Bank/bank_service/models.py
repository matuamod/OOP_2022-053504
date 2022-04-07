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


class Transfer(models.Model):
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )
    account_sender = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name='account_sender'
    )
    account_getter = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name='account_getter'
    )


class Frozen_acc(models.Model):
    account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name='frozen_account'
    )

    zero_flag = '0'
    first_flag = '1'

    FLAG_TYPE = (
        (zero_flag, '0'),
        (first_flag, '1'),
    )

    is_frozen_flag = models.CharField(
        max_length=1, verbose_name='Is frozen status', choices=FLAG_TYPE
    )

    @classmethod
    def make_frozen(cls, account, is_frozen_flag):
        if is_frozen_flag == '0':
            raise(ValueError('Account is not frozen now'))
        else:
            raise(ValueError('Account is frozen now'))


class Accumulation(models.Model):
    account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name='accumulated_account'
    )
    date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(
        decimal_places=2,
        max_digits=10
    )

    def __str__(self):
        return f'Accumulated account is {self.account}'


class Creditors(models.Model):
    user = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name='credit_account'
    )
    bank_acc = models.ForeignKey(
        Choose_bank,
        on_delete=models.CASCADE,
        related_name='bank'
    )
    amount = models.DecimalField(
        decimal_places=2,
        max_digits=10
    )
    
    first_credit_time = '3 month'
    sec_credit_time = '6 month'
    third_credit_time = '12 month'
    fourth_credit_time = '24 month'
    fifth_credit_time = '> than 24 month'

    CREDIT_TIME_TYPE = (
        (first_credit_time, '3 month'),
        (sec_credit_time, '6 month'),
        (third_credit_time, '12 month'),
        (fourth_credit_time, '24 month'),
        (fifth_credit_time, '> than 24 month'),
    )

    credit_time = models.CharField(
        max_length=20, 
        verbose_name='Credit time', 
        choices=CREDIT_TIME_TYPE
    )

    total_amount = models.DecimalField(
        decimal_places=2,
        max_digits=10, 
        default=0
    )