# Generated by Django 4.0.3 on 2022-04-04 13:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bank_type', '0001_initial'),
        ('bank_service', '0004_accumulation'),
    ]

    operations = [
        migrations.CreateModel(
            name='Creditors',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('credit_time', models.CharField(choices=[('3 month', '3 month'), ('6 month', '6 month'), ('12 month', '12 month'), ('24 month', '24 month'), ('> than 24 month', '> than 24 month')], max_length=20, verbose_name='Credit time')),
                ('total_amount', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('bank_acc', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bank', to='bank_type.choose_bank')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='credit_account', to='bank_service.account')),
            ],
        ),
    ]