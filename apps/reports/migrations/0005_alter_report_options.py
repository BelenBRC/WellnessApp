# Generated by Django 5.0.3 on 2024-06-13 15:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0004_alter_report_front_picture_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='report',
            options={'verbose_name': 'Reporte', 'verbose_name_plural': 'Reportes'},
        ),
    ]
