from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet

from apps.coach.models import Coach
from apps.client.models import Client

# Register your models here.
class ClientInline(admin.TabularInline):
    model = Client 
    list_display = ['full_name', 'city', 'age']
    extra = 0

# CoachUserAdminFilter will contain only coach users
class CoachUserAdminFilter(admin.SimpleListFilter):
    title = 'Usuario'
    parameter_name = 'user'
    
    def lookups(self, request, model_admin):
        coaches = set([coach.user for coach in Coach.objects.all()])
        return [(coach.id, coach.username) for coach in coaches]
    
    def queryset(self, request, queryset: QuerySet) -> QuerySet:
        if self.value():
            return queryset.filter(user=self.value())
        return queryset
    
class CoachAdmin(admin.ModelAdmin):
    inlines = [ClientInline]
    list_display = ['full_name_display', 'user_display', 'clients_count_display']
    search_fields = ['first_name', 'last_name', 'user__username']
    ordering = ['first_name', 'user__username']
    list_filter = ['first_name', 'last_name', CoachUserAdminFilter,]

    def clients_count_display(self, obj):
        return obj.clients_count
    clients_count_display.short_description = 'Nº clientes'
    
    def full_name_display(self, obj):
        return obj.full_name
    full_name_display.short_description = 'Nombre completo'
    
    def user_display(self, obj):
        return obj.user.username
    user_display.short_description = 'Usuario'

admin.site.register(Coach, CoachAdmin)