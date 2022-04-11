import decimal
from .models import Account, Transfer, Accumulation, Creditors
from django.db import transaction
from django.core.exceptions import ValidationError


def make_transfer(account_sender, account_getter, amount):

    if account_sender.balance < amount:
        raise(ValueError('Not enough money'))
    if account_sender == account_getter:
        raise(ValueError('Chose another account'))

    with transaction.atomic():
        from_balance = account_sender.balance - amount
        account_sender.balance = from_balance
        account_sender.save()

        to_balance = account_getter.balance + amount
        account_getter.balance = to_balance
        account_getter.save()

        transfer = Transfer.objects.create(
            account_sender=account_sender,
            account_getter=account_getter,
            amount=amount
        )

    return transfer


def filter_user_account(user, account_id):
    try:
        account = Account.objects.filter(
            user=user).get(pk=account_id)
    except (Account.DoesNotExist):
        raise ValidationError("Account doesn't exist")

    return account


def check_account_exists(account_id):
    try:
        account = Account.objects.get(pk=account_id)
    except Exception as e:
        print(e)
        raise ValueError('No such account')

    return account


def make_accumulation():
    accounts = Account.objects.all()
    for account in accounts:
        with transaction.atomic():
            pr = 0.08 / 12
            balance = float(account.balance)
            accumulation = balance * pr
            balance += accumulation
            account.balance = balance
            Accumulation.objects.create(
                account=account,
                amount=accumulation
            )
            account.save()


def print_hello():
    print('hello world!')


def make_credit_price(amount, credit_time):
    amount = float(amount)
    with transaction.atomic():
        if credit_time == '3 month':
            pr = 0.15
            total_amount = amount + amount * pr
        elif credit_time == '6 month':
            pr = 0.25
            total_amount = amount + amount * pr
        elif credit_time == '12 month':
            pr = 0.45
            total_amount = amount + amount * pr
        elif credit_time == '24 month':
            pr = 0.75
            total_amount = amount + amount * pr
        else:
            pr = 0.95
            total_amount = amount + amount * pr

        return decimal.Decimal(total_amount)
    

