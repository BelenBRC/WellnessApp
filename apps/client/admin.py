from django.contrib import admin

from apps.client.models import Client

# Register your models here.

class ClientAdmin(admin.ModelAdmin):
    list_display = ['full_name_display', 'user', 'coach', 'birthdate', 'city', 'occupation', 'age_display']
    list_filter = ['coach', 'city', 'occupation']
    search_fields = ['user__username', 'city', 'occupation']
    ordering = ['user__username', 'coach']
    
    def age_display(self, obj):
        return obj.age
    age_display.short_description = 'Edad'
    
    def full_name_display(self, obj):
        return obj.full_name
    full_name_display.short_description = 'Nombre completo'
    
admin.site.register(Client, ClientAdmin)