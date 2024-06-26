# Generated by Django 5.0.3 on 2024-06-06 17:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('client', '0003_client_first_name_client_last_name_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(help_text='Fecha del informe.', verbose_name='Fecha')),
                ('weight', models.FloatField(help_text='Peso actual en kilogramos.', verbose_name='Peso')),
                ('front_picture', models.ImageField(help_text='Foto frontal del cuerpo actualmente.', upload_to='reports/', verbose_name='Foto frontal')),
                ('right_side_picture', models.ImageField(help_text='Foto lateral derecha del cuerpo actualmente.', upload_to='reports/', verbose_name='Foto lateral derecha')),
                ('left_side_picture', models.ImageField(help_text='Foto lateral izquierda del cuerpo actualmente.', upload_to='reports/', verbose_name='Foto lateral izquierda')),
                ('training_compliance', models.PositiveSmallIntegerField(help_text='Del 1 al 10, ¿cómo calificaría el cumplimiento de entrenamiento? 1 es el peor y 10 el mejor.', verbose_name='Cumplimiento de entrenamiento')),
                ('training_satisfaction', models.PositiveSmallIntegerField(help_text='Del 1 al 10, ¿cómo calificaría la satisfacción con el entrenamiento? 1 es el peor y 10 el mejor.', verbose_name='Satisfacción con el entrenamiento')),
                ('diet_compliance', models.PositiveSmallIntegerField(help_text='Del 1 al 10, ¿cómo calificaría el cumplimiento de dieta? 1 es el peor y 10 el mejor.', verbose_name='Cumplimiento de dieta')),
                ('diet_satisfaction', models.PositiveSmallIntegerField(help_text='Del 1 al 10, ¿cómo calificaría la satisfacción con la dieta? 1 es el peor y 10 el mejor.', verbose_name='Satisfacción con la dieta')),
                ('diet_changes', models.TextField(help_text='¿Te gustaría añadir o eliminar algún alimento de tu dieta? ¿Por qué?', verbose_name='Cambios en la dieta')),
                ('training_observations', models.TextField(help_text='¿Qué ejercicios te han producido mejor sensación?¿Cuáles te han resultado más difíciles?', verbose_name='Observaciones del entrenamiento')),
                ('other_observations', models.TextField(help_text='¿Hay algo más que te gustaría compartir?', verbose_name='Otras observaciones')),
                ('client', models.ForeignKey(help_text='Cliente al que pertenece el reporte.', on_delete=django.db.models.deletion.CASCADE, related_name='reports', to='client.client', verbose_name='Cliente')),
            ],
        ),
    ]
