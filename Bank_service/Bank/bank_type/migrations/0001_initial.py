# Generated by Django 4.0.3 on 2022-03-25 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Choose_bank',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bank_name', models.CharField(choices=[('Superbank', 'Superbank'), ('Fastest-bank', 'Fastest-bank'), ('Goldbank', 'Goldbank')], default='default-bank', max_length=20, unique=True, verbose_name='Bank Name')),
                ('bank_iban', models.CharField(choices=[('SOS123456789', 'SOS123456789'), ('NAS333444787', 'NAS333444787'), ('RRRQ66666666', 'RRRQ66666666')], default='', max_length=20, unique=True, verbose_name='Bank IBAN')),
            ],
        ),
    ]
