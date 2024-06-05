from django.contrib import admin
from django import forms
from django.core.exceptions import ValidationError
from apps.training.models import GroupTraining, NamedGroup, OnlineTraining

class OnlineTrainingAdmin(admin.ModelAdmin):
    list_display = ('client_display', 'year', 'month', 'week')
    list_filter = ('client', 'year', 'month', 'week')
    search_fields = ('client__full_name', 'year', 'month', 'week')
    ordering = ('client', 'year', 'month', 'week')
    
    def client_display(self, obj):
        return obj.client.full_name
    client_display.short_description = 'Cliente'

class GroupTrainingAdminForm(forms.ModelForm):
    class Meta:
        model = GroupTraining
        fields = '__all__'

    # Custom validation for GroupTraining
    def clean(self):
        cleaned_data = super().clean()
        named_group = cleaned_data.get('named_group')
        components = cleaned_data.get('components')
        
        if not named_group and not components:
            raise ValidationError('Si no se ha seleccionado un grupo nombrado, debe añadir al menos un cliente.')


class GroupTrainingAdmin(admin.ModelAdmin):
    form = GroupTrainingAdminForm
    list_display = ('named_group', 'date', 'hour', 'number_of_clients_display', 'clients_list_display')
    ordering = ('named_group', 'date', 'hour')
    search_fields = ('named_group__name', 'date', 'hour')
    
    def number_of_clients_display(self, obj):
        return obj.number_of_clients()
    number_of_clients_display.short_description = 'Nº clientes'
    
    def clients_list_display(self, obj):
        return obj.clients_list()
    clients_list_display.short_description = 'Clientes'
    
class NamedGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'number_of_clients_display', 'clients_list_display')
    search_fields = ('name',)
    ordering = ('name',)
    
    def number_of_clients_display(self, obj):
        return obj.number_of_clients
    number_of_clients_display.short_description = 'Nº clientes'
    
    def clients_list_display(self, obj):
        return obj.clients_list
    clients_list_display.short_description = 'Clientes'
    
admin.site.register(OnlineTraining, OnlineTrainingAdmin)
admin.site.register(GroupTraining, GroupTrainingAdmin)
admin.site.register(NamedGroup, NamedGroupAdmin)