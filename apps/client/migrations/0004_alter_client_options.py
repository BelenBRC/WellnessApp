# Generated by Django 5.0.3 on 2024-06-13 15:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0003_client_first_name_client_last_name_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='client',
            options={'verbose_name': 'Cliente', 'verbose_name_plural': 'Clientes'},
        ),
    ]