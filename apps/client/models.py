import datetime
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    coach = models.ForeignKey('coach.Coach', on_delete=models.CASCADE, related_name='clients')
    
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
        null=False,
    )
    
    @property
    def age(self):
        return (datetime.date.today() - self.birthdate).days // 365
    
    def __str__(self):
        return self.user.username