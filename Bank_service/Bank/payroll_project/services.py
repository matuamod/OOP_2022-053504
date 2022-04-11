import decimal
from html import entities
from bank_service.models import Account
from .models import Add_worker, Payroll_project
from django.db import transaction
from django.core.exceptions import ValidationError

def find_entity_balance(user, company):  
    try:
        account = Account.objects.get(pk=company)
    except (Account.DoesNotExist):
        raise ValidationError("Account doesn't exist")

    return (account, account.balance)


def get_worker(worker):
    try:
        account = Account.objects.get(pk=worker)
    except (Account.DoesNotExist):
        raise ValidationError("Account doesn't exist")

    return account


def low_entity_balance(company, balance):
    accounts = Account.objects.all()
    with transaction.atomic():
        for account in accounts:
            if account.user == company.bank_name:
                if account.balance >= balance:
                    account.balance = balance  
                    account.save() 
                else:
                    raise ValueError('No such money on entity account')


def get_payroll_project(company, worker, balance, amount):
    accounts = Account.objects.all()
    with transaction.atomic():
        for account in accounts:
            if account.user == worker.bank_name:
                account.balance += amount
                balance -= amount
                account.save()
                low_entity_balance(company, balance)