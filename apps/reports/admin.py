from django.contrib import admin

from apps.reports.models import Report

# Register your models here.
class ReportAdmin(admin.ModelAdmin):
    list_display = ['client', 'date', 'weight']
    list_filter = ['client', 'date']
    search_fields = ['client__full_name', 'date']
    ordering = ['client', 'date']

admin.site.register(Report, ReportAdmin)