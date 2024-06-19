import datetime
from django import forms # type: ignore
from django.contrib.auth.forms import UserCreationForm # type: ignore
from django.contrib.auth.models import User, Group # type: ignore

from apps.client.models import Client

class LoginForm(forms.Form):
    username = forms.CharField(label='Username')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        
        if not username or not password:
            raise forms.ValidationError('Los campos de usuario y contraseña son obligatorios.')
        
        return cleaned_data
    

class ClientRegisterForm(UserCreationForm):
    """Form for registering a new user with client permissons."""
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
        
    # When create, the user will have the Client group permission
    def save(self, commit=True):
        user = super().save(commit=False)
        user.save()
        # Search for the group with the name 'Client'
        clientGroup = Group.objects.get(name='Client')
        if clientGroup:
            # Add the user to the group
            user.groups.add(clientGroup)
        # Set is_staff to False to ensure the user is not able to access the admin site
        user.is_staff = False
        
        return user
    
class CoachRegisterForm(UserCreationForm):
    """Form for registering a new user with coach permissions."""
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        
    #Set email as required, so the admin can contact the new coach
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True
        
    # When create, the user will have the Coach group permission
    def save(self, commit=True):
        user = super().save(commit=False)
        user.save()
        # Search for the group with the name 'Coach'
        coachGroup = Group.objects.get(name='Coach')
        if coachGroup:
            # Add the user to the group
            user.groups.add(coachGroup)
        # Set is_staff to False. 
        # The admin should give the user the permission to access the admin site
        user.is_staff = False
        
        return user
    
class ClientEditForm(forms.ModelForm):
    """Form for editing the client's profile."""
    class Meta:
        model = Client
        fields = ['first_name', 'last_name', 'city', 'occupation', 'birthdate']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            # Set help text as placeholder
            self.fields[field].widget.attrs['placeholder'] = self.fields[field].help_text
            if field == 'birthdate':
                self.fields[field].widget.attrs['placeholder'] += ' (dd/mm/yyyy)'
                # Set min value to 1900-01-01
                self.fields[field].widget.attrs['min'] = '1900-01-01'
                # Set max value to today
                self.fields[field].widget.attrs['max'] = datetime.date.today().strftime('%Y-%m-%d')
