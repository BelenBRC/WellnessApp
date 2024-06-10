from typing import Any
from django.contrib import admin
from django import forms
from django.core.exceptions import ValidationError
from django.db.models.fields import Field
from django.http.request import HttpRequest
from apps.exercise.models import GroupExerciseSet, OnlineExerciseSet
from apps.training.models import GroupTraining, NamedGroup, OnlineTraining

class ClientListFilter(admin.SimpleListFilter):
    title = 'Cliente'
    parameter_name = 'client'
    
    def lookups(self, request, model_admin):
        clients = set([training.client for training in OnlineTraining.objects.all()])
        if request.user.is_superuser:
            return [(client.id, client.full_name) for client in clients]
        else:
            # Select only clients of the coach
            return [(client.id, client.full_name) for client in clients if client.coach == request.user.coach]
    
    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(client=self.value())
        return queryset

class OnlineExerciseSetInline(admin.TabularInline):
    model = OnlineExerciseSet
    list_display = ['exercise', 'series_per_repetitions', 'rest', 'execution_method', 'observations',]
    list_filter = ['exercise', 'execution_method']
    ordering = ['exercise', 'series_per_repetitions', 'rest', 'execution_method', 'observations',]
    extra = 0
    
    # Custom formfield for observations field, so it displays smaller
    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super().formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'observations':
            formfield.widget = forms.Textarea(attrs={'cols': 20, 'rows': 2})
        return formfield

class OnlineTrainingAdmin(admin.ModelAdmin):
    inlines = [OnlineExerciseSetInline]
    list_display = ('client_display', 'year', 'month', 'week')
    list_filter = (ClientListFilter, 'year', 'month', 'week')
    search_fields = ('client__full_name', 'year', 'month')
    ordering = ('client', 'year', 'month')
    
    def client_display(self, obj):
        return obj.client.full_name
    client_display.short_description = 'Cliente'
    
    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super().formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'description':
            formfield.widget = forms.Textarea(attrs={'rows': 2})
        return formfield
    
    # Limit the results for coach view
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        # If not superuser, show only the ones of the coach
        return qs.filter(client__coach=request.user.coach)

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

class GroupExerciseSetInline(admin.TabularInline):
    model = GroupExerciseSet
    fields = ['client', 'exercise', 'series_per_repetitions', 'rest']
    exclude = ['execution_method', 'observations']
    extra = 0
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Show only components of the group training in client field if the instance is being modified
        if request.resolver_match.kwargs.get('object_id'):
            if db_field.name == 'client':    
                group_training = request.resolver_match.kwargs.get('object_id')
                group_training_instance = GroupTraining.objects.get(pk=group_training)
                kwargs['queryset'] = group_training_instance.components.all()

        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super().formfield_for_dbfield(db_field, **kwargs)
        print (db_field.name)
        if db_field.name == 'hour':
            formfield.widget = forms.Select(choices=[(hour, hour) for hour in range(6, 22)])
            print (formfield.widget.choices)
        return formfield

class GroupTrainingAdmin(admin.ModelAdmin):
    form = GroupTrainingAdminForm
    inlines = [GroupExerciseSetInline]
    list_display = ('group_coach', 'named_group', 'date', 'hour', 'number_of_clients_display', 'clients_list_display')
    ordering = ('date', 'hour', 'named_group')
    list_filter = ('date', 'hour', 'named_group')
    search_fields = ('named_group__name', 'date', 'hour')
    
    def number_of_clients_display(self, obj):
        return obj.number_of_clients
    number_of_clients_display.short_description = 'Nº clientes'
    
    def clients_list_display(self, obj):
        return obj.clients_list
    clients_list_display.short_description = 'Clientes'
    
    # Limit the results for coach view
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        # If not superuser, show only the ones of the coach
        return qs.filter(group_coach=request.user.coach)
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):              
        # If the request user is not superuser, show itself as the group coach
        if not request.user.is_superuser:
            if db_field.name == 'group_coach':
                kwargs['initial'] = request.user.coach
        
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super().formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'hour':
            formfield.widget = forms.Select(choices=[(hour, hour) for hour in range(6, 23)])
        return formfield
    
class NamedGroupAdminForm(forms.ModelForm):
    class Meta:
        model = NamedGroup
        fields = '__all__'
        
    
    
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