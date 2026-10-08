from django.urls import path
from django.contrib.auth import views as auth_views

from . import views


urlpatterns = [

    path(
        '',
        views.home,
        name='home'
    ),

    path(
        'register/',
        views.register_view,
        name='register'
    ),

    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='login.html'
        ),
        name='login'
    ),

    path(
        'logout/',
        auth_views.LogoutView.as_view(),
        name='logout'
    ),

    path(
        'jobs/',
        views.job_list,
        name='job_list'
    ),

    path(
        'jobs/<int:pk>/',
        views.job_detail,
        name='job_detail'
    ),

    path(
        'jobs/<int:pk>/apply/',
        views.apply_job,
        name='apply_job'
    ),

    path(
        'dashboard/',
        views.dashboard,
        name='dashboard'
    ),

    path(
        'profile/',
        views.profile,
        name='profile'
    ),

    path(
        'recruiter/jobs/add/',
        views.add_job,
        name='add_job'
    ),

    path(
        'recruiter/jobs/<int:pk>/edit/',
        views.edit_job,
        name='edit_job'
    ),

    path(
        'recruiter/jobs/<int:pk>/delete/',
        views.delete_job,
        name='delete_job'
    ),

    path(
        'recruiter/applications/<int:pk>/<str:status>/',
        views.update_application_status,
        name='update_application_status'
    ),
]