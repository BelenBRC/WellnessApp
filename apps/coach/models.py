from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Coach(models.Model):
    class Meta:
        verbose_name = 'Entrenador'
        verbose_name_plural = 'Entrenadores'
        
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
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
    
    def __str__(self):
        return self.full_name
    
    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'
    
    @property
    def clients_count(self):
        return self.clients.count()