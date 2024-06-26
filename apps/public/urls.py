from django.urls import include, path # type: ignore
from apps.public.views import index, login, register, coachRegister, logout, UserMainSpaceView, UserDetailView, UserReportsView, UserOnlineTrainingView, UserReportDetailView, new_report_view, UserOnlineTrainingDetailView

urlpatterns = [ 
    path("", index, name="index"),
    
    path("login/", login, name="login"),
    path("logout/", logout, name="logout"),
    
    path("register/", register, name="register"),
    path("coach_register/", coachRegister, name="coach_register"),
]

# Private views after login
urlpatterns += [
    path("area_personal/", UserMainSpaceView.as_view(), name="user_main_space"),
    path(
        "area_personal/",
        include(
            [
                path("perfil/", UserDetailView.as_view(), name="user_detail"), 
                path("informes/", UserReportsView.as_view(), name="user_reports"),
                path("informes/nuevo/", new_report_view, name="new_report"),
                path("informes/<id_report>/", UserReportDetailView.as_view(), name="report_detail"),
                path("entrenamientos/", UserOnlineTrainingView.as_view(), name="user_online_trainings"),
                path("entrenamientos/<id_training>/", UserOnlineTrainingDetailView.as_view(), name="training_detail"),
            ]
        ), 
    ),
]