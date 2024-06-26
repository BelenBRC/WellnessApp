from django.db import models

# Create your models here.
class MuscularGroup(models.Model):
    class Meta:
        verbose_name = 'Grupo muscular'
        verbose_name_plural = 'Grupos musculares'
        
    name = models.CharField(
        verbose_name='Nombre',
        help_text='Nombre del grupo muscular.',
        max_length=100,
        unique=True,
    )
    
    def __str__(self):
        return self.name
    
    
class Objective(models.Model):
    class Meta:
        verbose_name = 'Objetivo'
        verbose_name_plural = 'Objetivos'
        
    name = models.CharField(
        verbose_name='Nombre',
        help_text='Nombre del objetivo.',
        max_length=100,
        unique=True,
    )
    
    def __str__(self):
        return self.name
    
    
class Exercise(models.Model):
    class Meta:
        verbose_name = 'Ejercicio'
        verbose_name_plural = 'Ejercicios'
        
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
    class Meta:
        verbose_name = 'Método de ejecución'
        verbose_name_plural = 'Métodos de ejecución'
        
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
    
    rest = models.CharField(
        verbose_name='Descanso',
        help_text='Tiempo de descanso entre series.',
        max_length=50,
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
    
class OnlineExerciseSet(ExerciseSet):
    online_training = models.ForeignKey(
        'training.OnlineTraining', 
        on_delete=models.CASCADE, 
        related_name='exercises',
        verbose_name='Entrenamiento online',
        help_text='Entrenamiento online al que pertenece la serie.',
    )
    
class GroupExerciseSet(ExerciseSet):
    client = models.ForeignKey(
        'client.Client', 
        on_delete=models.CASCADE, 
        related_name='group_sets',
        verbose_name='Cliente',
        help_text='Cliente del grupo al que pertenece la serie.',
        null=True,
    )
    
    group_training = models.ForeignKey(
        'training.GroupTraining', 
        on_delete=models.CASCADE, 
        related_name='exercises',
        verbose_name='Entrenamiento en grupo',
        help_text='Entrenamiento en grupo al que pertenece la serie.',
        null=True,
    )