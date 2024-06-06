import datetime
import os
from django.db import models

def get_upload_to_front(instance, filename):
    return get_upload_to(instance, filename, 'front')

def get_upload_to_right(instance, filename):
    return get_upload_to(instance, filename, 'right')

def get_upload_to_left(instance, filename):
    return get_upload_to(instance, filename, 'left')

def get_upload_to(instance, filename, side):
    # Get the current date
    today = datetime.date.today().strftime('%Y.%m.%d')
    # Get client id
    client_id = instance.client.id
    # Get the extension of the file
    _, extension = os.path.splitext(filename)
    # New filename
    new_filename = f'{today}-{side}{extension}'
    #Return the path
    return os.path.join('static','reports', str(client_id), new_filename)
    

# Create your models here.
class Report(models.Model):
    client = models.ForeignKey(
        'client.Client', 
        on_delete=models.CASCADE, 
        related_name='reports',
        verbose_name='Cliente',
        help_text='Cliente al que pertenece el reporte.',
    )
    
    # This field is not editable, it is set automatically
    date = models.DateField(
        verbose_name='Fecha',
        help_text='Fecha del informe.',
        default=datetime.date.today,
        null=False,
        editable=False,
    )
    
    weight = models.FloatField(
        verbose_name='Peso',
        help_text='Peso actual en kilogramos.',
        null=False,
    )
    
    # Body pictures
    front_picture = models.ImageField(
        verbose_name='Foto frontal',
        help_text='Foto frontal del cuerpo actualmente.',
        upload_to=get_upload_to_front,
        null=False,
    )
    
    right_side_picture = models.ImageField(
        verbose_name='Foto lateral derecha',
        help_text='Foto lateral derecha del cuerpo actualmente.',
        upload_to=get_upload_to_right,
        null=False,
    )
    
    left_side_picture = models.ImageField(
        verbose_name='Foto lateral izquierda',
        help_text='Foto lateral izquierda del cuerpo actualmente.',
        upload_to=get_upload_to_left,
        null=False,
    )
    
    # Survey 1-10 fields
    training_compliance = models.PositiveSmallIntegerField(
        verbose_name='Cumplimiento de entrenamiento',
        help_text='Del 1 al 10, ¿cómo calificaría el cumplimiento de entrenamiento? 1 es el peor y 10 el mejor.',
        null=False,
    )
    
    training_satisfaction = models.PositiveSmallIntegerField(
        verbose_name='Satisfacción con el entrenamiento',
        help_text='Del 1 al 10, ¿cómo calificaría la satisfacción con el entrenamiento? 1 es el peor y 10 el mejor.',
        null=False,
    )
    
    diet_compliance = models.PositiveSmallIntegerField(
        verbose_name='Cumplimiento de dieta',
        help_text='Del 1 al 10, ¿cómo calificaría el cumplimiento de dieta? 1 es el peor y 10 el mejor.',
        null=False,
    )
    
    diet_satisfaction = models.PositiveSmallIntegerField(
        verbose_name='Satisfacción con la dieta',
        help_text='Del 1 al 10, ¿cómo calificaría la satisfacción con la dieta? 1 es el peor y 10 el mejor.',
        null=False,
    )
    
    # Text fields
    diet_changes = models.TextField(
        verbose_name='Cambios en la dieta',
        help_text='¿Te gustaría añadir o eliminar algún alimento de tu dieta? ¿Por qué?',
        null=True,
        blank=True,
    )
    
    training_observations = models.TextField(
        verbose_name='Observaciones del entrenamiento',
        help_text='¿Qué ejercicios te han producido mejor sensación?¿Cuáles te han resultado más difíciles?',
        null=True,
        blank=True,
    )
    
    other_observations = models.TextField(
        verbose_name='Otras observaciones',
        help_text='¿Hay algo más que te gustaría compartir?',
        null=True,
        blank=True,
    )
    
    def __str__(self):
        return f'Reporte {self.client} {self.date}'