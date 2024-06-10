from collections.abc import Sequence
from datetime import date
from typing import Any
from django import forms
from django.contrib import admin
from django.db.models.fields import Field
from django.http.request import HttpRequest

from apps.client.models import Client
from apps.reports.models import Report

# Register your models here.

class UserClientListFilter(admin.SimpleListFilter):
    title = 'Usuario'
    parameter_name = 'user'
    
    def lookups(self, request, model_admin):
        users = set([client.user for client in Client.objects.all()])
        if request.user.is_superuser:
            # Show only clients with Client group
            return [(user.id, user.username) for user in users if user.groups.filter(name='Client').exists()]
        else:
            # Select only clients of the coach
            return [(user.id, user.username) for user in users if user.client.coach == request.user.coach]
    
    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(user=self.value())
        return queryset

class ReportInline(admin.TabularInline):
    model = Report
    extra = 0
    fields = ['date', 'weight', 'training_compliance', 'training_satisfaction', 'diet_compliance', 'diet_satisfaction', 'diet_changes', 'training_observations', 'other_observations', 'front_picture', 'right_side_picture', 'left_side_picture']
    readonly_fields = ['date']
    ordering = ['-date']
    
    # Smaller text area
    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super().formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'diet_changes' or db_field.name == 'training_observations' or db_field.name == 'other_observations':
            formfield.widget = forms.Textarea(attrs={'rows': 3, 'cols': 15})
        
        return formfield

class ClientAdmin(admin.ModelAdmin):
    inlines = [ReportInline]
    list_display = ['full_name_display', 'user', 'coach', 'birthdate', 'city', 'occupation', 'age_display']
    list_filter = ['coach', 'city', UserClientListFilter]
    search_fields = ['user__username', 'city', 'occupation']
    ordering = ['user__username', 'coach']
    
    def age_display(self, obj):
        return obj.age
    age_display.short_description = 'Edad'
    
    def full_name_display(self, obj):
        return obj.full_name
    full_name_display.short_description = 'Nombre completo'
    
    # Limit the results for coach view
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs.filter(user__groups__name='Client')
        # If not superuser, show only clients of the coach
        return qs.filter(coach=request.user.coach)
    
    # List filter for coach view
    def get_list_filter(self, request: HttpRequest) -> Sequence[str]:
        if request.user.is_superuser:
            return self.list_filter
        else:
            return ['city', UserClientListFilter]
        
    # Formset change to limit the dropdown list to the clients of the coach
    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super().formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'user':
            # Show only the users with no client assigned and with Client group
            formfield.queryset = formfield.queryset.filter(groups__name='Client')
            formfield.queryset = formfield.queryset.exclude(client__isnull=False)
            
        # If coach user, set itself as coach
        if db_field.name == 'coach' and not kwargs['request'].user.is_superuser:
            formfield.initial = kwargs['request'].user.coach  
            
        # For city, show a select with spanish cities
            
        return formfield
            
admin.site.register(Client, ClientAdmin)