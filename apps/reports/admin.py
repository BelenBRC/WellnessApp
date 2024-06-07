from django.contrib import admin

from apps.reports.models import Report

# Register your models here.
class ClientListFilter(admin.SimpleListFilter):
    title = 'Cliente'
    parameter_name = 'client'
    
    def lookups(self, request, model_admin):
        clients = set([report.client for report in Report.objects.all()])
        if request.user.is_superuser:
            return [(client.id, client.full_name) for client in clients]
        else:
            # Select only clients of the coach
            return [(client.id, client.full_name) for client in clients if client.coach == request.user.coach]
    
    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(client=self.value())
        return queryset

class ReportAdmin(admin.ModelAdmin):
    list_display = ['client', 'date', 'weight']
    list_filter = [ClientListFilter, 'date']
    search_fields = ['client__full_name', 'date']
    ordering = ['client', 'date']
    
    # Limit the results for coach view
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        # If not superuser, show only reports of the coach
        return qs.filter(client__coach=request.user.coach)

admin.site.register(Report, ReportAdmin)