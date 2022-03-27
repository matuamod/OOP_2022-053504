from tabnanny import verbose
from django.db import models
from django.conf import settings


class Choose_bank(models.Model):

    first_bank_name = 'Superbank'
    first_bank_iban = 'SOS123456789'
    sec_bank_name = 'Fastest-bank'
    sec_bank_iban = 'NAS333444787'
    third_bank_name = 'Goldbank'
    third_bank_iban = 'RRRQ66666666'

    BANK_NAME = (
        (first_bank_name, 'Superbank'),
        (sec_bank_name, 'Fastest-bank'),
        (third_bank_name, 'Goldbank')
    )

    bank_name = models.CharField(max_length=20, verbose_name='Bank Name',
                                 choices=BANK_NAME, default='default-bank', unique=True)

    BANK_IBAN = (
        (first_bank_iban, 'SOS123456789'),
        (sec_bank_iban, 'NAS333444787'),
        (third_bank_iban, 'RRRQ66666666')
    )

    bank_iban = models.CharField(
        max_length=20, verbose_name='Bank IBAN', choices=BANK_IBAN, default='', unique=True)

    def __str__(self):
        return self.bank_name
