from django.contrib import admin

from apps.coach.models import Coach
from apps.client.models import Client

# Register your models here.
class ClientInline(admin.TabularInline):
    model = Client 
    list_display = ['full_name', 'city', 'age']
    extra = 0
    
class CoachAdmin(admin.ModelAdmin):
    inlines = [ClientInline]
    list_display = ['full_name_display', 'user_display', 'clients_count_display']
    search_fields = ['name', 'last_name', 'user__username']
    ordering = ['first_name', 'user__username']

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