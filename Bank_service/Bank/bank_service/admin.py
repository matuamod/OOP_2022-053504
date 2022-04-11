from django.contrib import admin
from bank_service.models import (
    Individual, Entity, Account, Action, Transaction, Transfer, Frozen_acc, Creditors
)
# Register your models here.
admin.site.register(Individual)
admin.site.register(Entity)
admin.site.register(Account)
admin.site.register(Action)
admin.site.register(Transaction)
admin.site.register(Transfer)
admin.site.register(Frozen_acc)
admin.site.register(Creditors)
