import datetime
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Client(models.Model):
    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
    
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE,
        verbose_name='Usuario',
        help_text='Usuario registrado asociado al cliente.',
    )
    
    coach = models.ForeignKey(
        'coach.Coach', 
        on_delete=models.CASCADE, 
        related_name='clients',
        verbose_name='Entrenador',
        help_text='Entrenador asignado al cliente.',
    )
    
    # Personal Information
    birthdate = models.DateField(
        verbose_name='Fecha de nacimiento',
        help_text='Por favor, introduzca su fecha de nacimiento.',
        null=False,
    )
    city = models.CharField(
        verbose_name='Ciudad',
        help_text='Por favor, introduzca su ciudad de residencia.',
        max_length=100,
        null=False,
    )
    occupation = models.CharField(
        verbose_name='Ocupación',
        help_text='Por favor, introduzca su ocupación.',
        max_length=100,
        null=True,
        blank=True,
    )
    first_name = models.CharField(
        verbose_name='Nombre',
        help_text='Por favor, introduzca su nombre.',
        max_length=100,
        null=False,
        default='',
    )
    last_name = models.CharField(
        verbose_name='Apellidos',
        help_text='Por favor, introduzca sus apellidos.',
        max_length=100,
        null=False,
        default='',
    )
    
    @property
    def age(self):
        return (datetime.date.today() - self.birthdate).days // 365
    
    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'
    
    def __str__(self):
        return self.full_name