# Generated by Django 5.0.3 on 2024-06-05 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exercise', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='method',
            name='name',
            field=models.CharField(help_text='Nombre del método.', max_length=100, unique=True, verbose_name='Nombre'),
        ),
        migrations.AlterField(
            model_name='musculargroup',
            name='name',
            field=models.CharField(help_text='Nombre del grupo muscular.', max_length=100, unique=True, verbose_name='Nombre'),
        ),
        migrations.AlterField(
            model_name='objective',
            name='name',
            field=models.CharField(help_text='Nombre del objetivo.', max_length=100, unique=True, verbose_name='Nombre'),
        ),
    ]
