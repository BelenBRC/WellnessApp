# Generated by Django 5.0.3 on 2024-06-05 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0002_alter_client_coach'),
        ('training', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='namedgroup',
            name='components',
            field=models.ManyToManyField(related_name='named_groups', to='client.client'),
        ),
        migrations.AlterField(
            model_name='onlinetraining',
            name='month',
            field=models.PositiveSmallIntegerField(default=6, help_text='Mes del entrenamiento.', verbose_name='Mes'),
        ),
        migrations.AlterField(
            model_name='onlinetraining',
            name='year',
            field=models.PositiveSmallIntegerField(default=2024, help_text='Año del entrenamiento.', verbose_name='Año'),
        ),
        migrations.DeleteModel(
            name='PersonGroupTraining',
        ),
    ]
