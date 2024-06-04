from django.contrib import admin

from apps.client.models import Client

# Register your models here.

class ClientAdmin(admin.ModelAdmin):
    list_display = ['user', 'coach', 'birthdate', 'city', 'occupation', 'age']
    list_filter = ['coach', 'city', 'occupation']
    search_fields = ['user__username', 'city', 'occupation']
    ordering = ['user__username']
    
admin.site.register(Client, ClientAdmin)