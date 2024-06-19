import datetime
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout # type: ignore
from django.contrib.auth.decorators import login_required # type: ignore
from django.db.models.base import Model as Model # type: ignore
from django.shortcuts import redirect, render # type: ignore
from django.utils.decorators import method_decorator # type: ignore
from django.views.generic import TemplateView # type: ignore

from apps.client.models import Client
from apps.coach.models import Coach
from apps.public.forms.loginforms import ClientEditForm, ClientRegisterForm, CoachRegisterForm, LoginForm
from apps.reports.forms import NewReportForm
from apps.reports.models import Report
from apps.training.models import OnlineTraining

####################################################################################################
def index(request):
    # If user not authenticated, redirect to login
    if not request.user.is_authenticated:
        return redirect('login')
    
    # If user is staff, redirect to admin
    if request.user.is_staff:
        return redirect('admin:index')
    
    # If user is client, redirect to user main space
    if hasattr(request.user, 'client'):
        return redirect('user_main_space')

####################################################################################################
################ LOGIN AND REGISTER VIEWS ##########################################################
####################################################################################################

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
            if user.is_staff:
                return redirect('admin:index')

            return redirect('user_main_space')
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

####################################################################################################
################ USER PRIVATE VIEWS ################################################################
####################################################################################################

# Login required views
@method_decorator(login_required, name='dispatch')
class UserMainSpaceView(TemplateView):
    template_name = 'private/user_main_space.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Área personal'
        
        # Search the client
        client = Client.objects.filter(user=self.request.user).first()
        context['client'] = client
        
        # Search the reports
        reports = Report.objects.filter(client=client)
        context['reports'] = reports
        
        # Search the online trainings
        trainings = OnlineTraining.objects.filter(client=client)
        context['trainings'] = trainings
        
        # Latest training
        latest_training = trainings.last()
        for training in trainings:
            if training.date > latest_training.date:
                latest_training = training
        
        context['latest_training'] = latest_training
        
        return context

# User detail
@method_decorator(login_required, name='dispatch')
class UserDetailView(TemplateView):
    model = Client
    template_name = 'private/user_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Perfil'
        
        # Search the client
        client = Client.objects.filter(user=self.request.user).first()
        context['client'] = client
        
        # Get the form
        form = ClientEditForm(instance=client)
        context['form'] = form
        
        # Get the reports
        reports = Report.objects.filter(client=client)
        context['reports'] = reports
        
        return context
    
    # Form to edit the client
    def post(self, request, *args, **kwargs):
        # Search the client
        client = Client.objects.filter(user=self.request.user).first()
        context = self.get_context_data()
        context['client'] = client
        
        # Get the form
        form = ClientEditForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            form = ClientEditForm(instance=client)
            context['form'] = form
            context['success'] = 'Cambios guardados correctamente.'
        else:
            context['error'] = form.errors
            context['form'] = form
            
        return render(request, 'private/user_detail.html', context) 
    
# User reports
@method_decorator(login_required, name='dispatch')
class UserReportsView(TemplateView):
    template_name = 'private/user_reports.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Informes'
        
        # Search the client
        client = Client.objects.filter(user=self.request.user).first()
        context['client'] = client
        
        # Search the reports
        reports = Report.objects.filter(client=client)
        context['reports'] = reports
        
        # Get the form
        form = NewReportForm()
        context['form'] = form
        
        return context
    
    # Form to create a new report
    def post(self, request, *args, **kwargs):
        # Search the client
        client = Client.objects.filter(user=self.request.user).first()
        context = self.get_context_data()
        context['client'] = client
        
        # Get the form
        form = NewReportForm(request.POST, request.FILES)
        if form.is_valid():
            report = form.save(commit=False)
            report.client = client
            report.date = datetime.date.today()
            report.save()
            
            # Redirect to the report detail, with the new report
            return redirect('report_detail', id_report=report.id)
        else:
            context['form'] = form
            context['error'] = form.errors
            
        return render(request, 'private/user_reports.html', context)

@method_decorator(login_required, name='dispatch')
class UserReportDetailView(TemplateView):
    model = Report
    template_name = 'private/report_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Informe'
        
        # Search the client
        client = Client.objects.filter(user=self.request.user).first()
        context['client'] = client
        
        # Search the report
        report = Report.objects.filter(id=kwargs['id_report']).first()
        context['report'] = report
        
        return context
    
def new_report_view(request):
    # If the user is not authenticated, redirect to login
    if not request.user.is_authenticated:
        return redirect('login')
    
    context = {
        'form': NewReportForm(),
        'title': 'Nuevo informe',
    }
    
    if request.method == 'POST':
        form = NewReportForm(request.POST, request.FILES)
        if form.is_valid():
            report = form.save(commit=False)
            report.client = Client.objects.filter(user=request.user).first()
            report.date = datetime.date.today()
            report.save()
            
            # Redirect to the report detail, with the new report
            return redirect('report_detail', id_report=report.id)
        else:
            context['form'] = form
            context['error'] = form.errors
    
    return render(request, 'private/new_report.html', context)
    
# User online training
@method_decorator(login_required, name='dispatch')
class UserOnlineTrainingView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Entrenamiento online'
        return context
    
    def get(self, request, *args, **kwargs):
        # Search the client
        client = request.user.client
        
        context = self.get_context_data()
        context['client'] = client
        
        # Search the online trainings
        trainings = OnlineTraining.objects.filter(client=client)
        context['trainings'] = trainings
            
        # Latest training
        latest_training = trainings.last()
        for training in trainings:
            if training.date > latest_training.date:
                latest_training = training
        
        context['latest_training'] = latest_training
        
        return render(request, 'private/user_online_trainings.html', context)
    
    def post(self, request, *args, **kwargs):
        # Search the client
        client = request.user.client
        
        context = self.get_context_data()
        context['client'] = client
        return render(request, 'private/user_online_trainings.html', context)
    
@method_decorator(login_required, name='dispatch')
class UserOnlineTrainingDetailView(TemplateView):
    model = OnlineTraining
    template_name = 'private/training_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Entrenamiento online'
        
        # Search the client
        client = Client.objects.filter(user=self.request.user).first()
        context['client'] = client
        
        # Search the online training
        training = OnlineTraining.objects.filter(id=kwargs['id_training']).first()
        context['training'] = training
        
        # Get the exercises
        exercises = training.exercises.all()
        context['exercises'] = exercises
        
        return context