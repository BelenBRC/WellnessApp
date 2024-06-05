import datetime
from django.core.exceptions import ValidationError
from django.db import models

class BasePersonalTraining(models.Model):
    client = models.ForeignKey('client.Client', on_delete=models.CASCADE, related_name='trainings')
    
    description = models.TextField(
        verbose_name='Descripción',
        help_text='Descripción del entrenamiento.',
        null=True,
        blank=True,
    )
    
    duration = models.CharField(
        verbose_name='Duración',
        help_text='Duración del entrenamiento.',
        max_length=50,
        null=True,
        blank=True,
    )

class OnlineTraining(BasePersonalTraining):
    year = models.PositiveSmallIntegerField(
        verbose_name='Año',
        help_text='Año del entrenamiento.',
        null=False,
        default=datetime.date.today().year,
    )
        
    month = models.PositiveSmallIntegerField(
        verbose_name='Mes',
        help_text='Mes del entrenamiento.',
        null=False,
        default=datetime.date.today().month,
    )
    
    week = models.PositiveSmallIntegerField(
        verbose_name='Semana',
        help_text='Semana del mes.',
        null=True,
        blank=True,
    )
    
    def __str__(self):        
        if self.week:
            return f' {self.client.full_name} | {self.month}/{self.year} | semana {self.week}'
        return f' {self.client.full_name} | {self.month}/{self.year}'
    
    @property
    def exercises_count(self):
        return self.exercises.count()
    

class GroupTraining(models.Model):
    #Optional named group
    named_group = models.ForeignKey(
        'training.NamedGroup', 
        on_delete=models.CASCADE, 
        related_name='group_trainings', 
        null=True, 
        blank=True,
        verbose_name='Grupo nombrado',
        help_text='Los clientes de este grupo se añadirán automáticamente.',
    )
    
    date = models.DateField(
        verbose_name='Fecha',
        help_text='Fecha del entrenamiento.',
        null=False,
    )
    
    hour = models.PositiveSmallIntegerField(
        verbose_name='Hora',
        help_text='Hora del entrenamiento.',
        null=False,
    )
    
    # Components are the clients that are part of the group
    # If the group is named, the components are the clients that are part of the named group plus the clients that are part of the group
    components = models.ManyToManyField(
        'client.Client', 
        related_name='group_trainings',
        verbose_name='Clientes extra',
        help_text='Si se ha seleccionado un grupo nombrado, no es obligatorio.',
        blank=True,
    )
    
    def __str__(self):
        if self.named_group:
            return f' {self.named_group} | {self.date} | {self.hour}:00 '
        return f' {self.date} | {self.hour}:00'
        
    def number_of_clients(self):
        number = self.components.count()
        if self.named_group:
            number += self.named_group.number_of_clients
        
        return number
        
    def clients_list(self):
        # If the group is named, the clients are the clients that are part of the named group plus the clients that are part of the group
        clients = list(self.components.all())
        
        if self.named_group:
            # Don't show the clients that are already in the group
            for client in self.named_group.components.all():
                if client not in clients:
                    clients.append(client)
        
        return [client for client in clients]
            
    
class NamedGroup(models.Model):
    name = models.CharField(
        verbose_name='Nombre',
        help_text='Nombre del grupo.',
        null=True,
        blank=True,
        max_length=50,
    )
    
    components = models.ManyToManyField(
        'client.Client', 
        related_name='named_groups', 
        verbose_name='Clientes', 
        help_text='Clientes que pertenecen al grupo.',
    )
    
    def __str__(self):
        return f' {self.name}'
    
    @property
    def number_of_clients(self):
        return self.components.count()
    
    @property
    def clients_list(self):
        if self.number_of_clients == 0:
            return 'No hay clientes en este grupo.'
        else:
            return [client for client in self.components.all()]