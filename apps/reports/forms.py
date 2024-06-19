from django import forms # type: ignore
from apps.reports.models import Report

class NewReportForm(forms.ModelForm):
    class Meta:
        model = Report
        exclude = ['client', 'date']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
            
            if field == 'weight':
                self.fields[field].widget.attrs.update({'step': '0.01'})
                self.fields[field].label = 'Peso (kg)'
                self.fields[field].widget.attrs.update({'min': '20.00'})
                
            if field == 'training_compliance' or field == 'training_satisfaction' or field == 'diet_compliance' or field == 'diet_satisfaction':
                self.fields[field].widget.attrs.update({'min': '0', 'max': '10'})
                self.fields[field].label += ' (0-10)'
                self.fields[field].value = 0
                
            if isinstance(self.fields[field].widget, forms.Textarea):
                self.fields[field].widget.attrs.update({'rows': '4'})
                self.fields[field].widget.attrs.update({'placeholder': self.fields[field].help_text})