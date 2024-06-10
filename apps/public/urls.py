from django.urls import path
from apps.public.views import IndexView, login, register, coachRegister, logout

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("login/", login, name="login"),
    path("logout/", logout, name="logout"),
    path("register/", register, name="register"),
    path("coach_register/", coachRegister, name="coach_register"),
]