from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render
from django.views.generic import TemplateView

from apps.public.forms.loginforms import ClientRegisterForm, CoachRegisterForm, LoginForm

class IndexView(TemplateView):
    template_name = 'index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # If the user is authenticated, add the user to the context
        if self.request.user.is_authenticated:
            context['user'] = self.request.user
        else:
            context['user'] = None
        
        context['title'] = 'Home'
        return context

def login(request):
    # If the user is already logged in, redirect to the index
    if request.user.is_authenticated:
        return redirect('index')
    
    context={
        'form': LoginForm(),
    }
    
    if request.method == 'POST':
        user = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=user, password=password)
        
        if user is not None:
            auth_login(request, user)
            return redirect('index')
        else:
            context['error'] = 'Usuario o contraseña incorrectos.'
    
    return render(request, 'login.html', context)

def logout(request):
    auth_logout(request)
    # Redirect to the index with new context
    return redirect('index')

def register(request):
    context={
        'form': ClientRegisterForm(),
    }
    
    if request.method == 'POST':
        form = ClientRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
            #TODO: Change the redirect to the personal space
        else:
            context['form'] = form
            context['error'] = form.errors
    
    return render(request, 'register.html', context)

def coachRegister(request):
    context={
        'form': CoachRegisterForm(),
    }
    
    if request.method == 'POST':
        form = CoachRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
            #TODO: Change the redirect to the admin site
        else:
            context['form'] = form
            context['error'] = form.errors
    
    return render(request, 'register.html', context)