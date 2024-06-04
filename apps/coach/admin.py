from django.contrib import admin

from apps.coach.models import Coach
from apps.client.models import Client

# Register your models here.
class ClientInline(admin.TabularInline):
    model = Client 
    extra = 0
    
class CoachAdmin(admin.ModelAdmin):
    inlines = [ClientInline]
    list_display = ['user', 'clients_count']
    search_fields = ['user__username']
    ordering = ['user__username']

admin.site.register(Coach, CoachAdmin)