from django.db import models

# Create your models here.
class MuscularGroup(models.Model):
    name = models.CharField(
        verbose_name='Nombre',
        help_text='Nombre del grupo muscular.',
        max_length=100,
        unique=True,
    )
    
    def __str__(self):
        return self.name
    
    
class Objective(models.Model):
    name = models.CharField(
        verbose_name='Nombre',
        help_text='Nombre del objetivo.',
        max_length=100,
        unique=True,
    )
    
    def __str__(self):
        return self.name
    
    
class Exercise(models.Model):
    name = models.CharField(
        verbose_name='Nombre',
        help_text='Nombre del ejercicio.',
        max_length=100,
    )
    
    description = models.TextField(
        verbose_name='Descripción',
        help_text='Descripción del ejercicio.',
        null=True,
        blank=True,
    )
    
    video = models.URLField(
        verbose_name='Vídeo',
        help_text='URL del vídeo.',
        null=True,
        blank=True,
    )
    
    muscular_group = models.ForeignKey(
        'MuscularGroup', 
        on_delete=models.CASCADE, 
        related_name='exercises',
        verbose_name='Grupo muscular',
        help_text='Grupo muscular al que pertenece el ejercicio.',
        null=True,
        blank=True,
    )
    
    objective = models.ForeignKey(
        'Objective', 
        on_delete=models.CASCADE, 
        related_name='exercises',
        verbose_name='Objetivo',
        help_text='Objetivo del ejercicio.',
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name
    
    @property
    def has_video(self):
        return bool(self.video)
    
    
class Method(models.Model):
    name = models.CharField(
        verbose_name='Nombre',
        help_text='Nombre del método.',
        max_length=100,
        unique=True,
    )
    
    description = models.TextField(
        verbose_name='Descripción',
        help_text='Descripción del método.',
        null=True,
        blank=True,
    )
    
    def __str__(self):
        return self.name
    
class ExerciseSet(models.Model):
    exercise = models.ForeignKey(
        'Exercise', 
        on_delete=models.CASCADE, 
        related_name='exercise_sets',
        verbose_name='Ejercicio',
        help_text='Ejercicio al que pertenece la serie.',
    )
    
    series_per_repetitions = models.CharField(
        verbose_name='Series X Repeticiones',
        help_text='Descripción de las series y repeticiones o tiempo.',
        max_length=50,
        null=True,
        blank=True,
    )
    
    rest = models.DurationField(
        verbose_name='Descanso',
        help_text='Tiempo de descanso entre series.',
        null=True,
        blank=True,
    )
    
    observations = models.TextField(
        verbose_name='Observaciones',
        help_text='Observaciones del ejercicio.',
        null=True,
        blank=True,
    )
    
    execution_method = models.ForeignKey(
        'Method', 
        on_delete=models.CASCADE, 
        related_name='exercise_sets',
        verbose_name='Método de ejecución',
        help_text='Método de ejecución del ejercicio.',
        null=True,
        blank=True,
    )
    
    def __str__(self):
        if self.series_per_repetitions:
            return f'{self.exercise.name} | {self.series_per_repetitions}'
        return self.exercise.name