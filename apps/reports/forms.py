from django import forms
from apps.reports.models import Report

class NewReportForm(forms.ModelForm):
    class Meta:
        model = Report
        exclude = ['client', 'date']