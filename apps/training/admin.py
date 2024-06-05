from django.contrib import admin
from django import forms
from django.core.exceptions import ValidationError
from apps.exercise.models import GroupExerciseSet, OnlineExerciseSet
from apps.training.models import GroupTraining, NamedGroup, OnlineTraining

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
    list_filter = ('client', 'year', 'month', 'week')
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
    
    # Show only components of the group training in client field
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'client':    
            group_training = request.resolver_match.kwargs.get('object_id')
            group_training_instance = GroupTraining.objects.get(pk=group_training)
            kwargs['queryset'] = group_training_instance.components.all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

class GroupTrainingAdmin(admin.ModelAdmin):
    form = GroupTrainingAdminForm
    inlines = [GroupExerciseSetInline]
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