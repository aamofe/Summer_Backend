

from django.urls import path

from . import views
from .views import *

urlpatterns = [
    path('create_team/', views.create_team, name='create_team'),
    path('update_team/',views.update_team),
    path('checkout_team/',views.checkout_team),
    path('get_current_team/',views.get_current_team),
    path('get_invitation/', views.get_invitation, name='get_invitation'),
    path('accept_invitation/<str:token>/', views.accept_invitation, name='accept_invitation'),
    path('team_name/<str:token>',views.team_name),
    path('all_teams/', views.all_teams, name='get_teams'),
    path('all_members/', views.all_members, name='get_members'),
    path('update_permisson/<str:team_id>/',views.update_permisson),
    path('create_project/<int:team_id>/',views.create_project),
    path('delete_one_project/',views.delete_one_project),
    path('rename_project/',views.rename_project),
    path('all_projects/',views.all_projects),
    path('get_one_team/',views.get_one_team),
    path('quit_team/',views.quit_team),
    path('all_deleted_project/',views.all_deleted_project),
    path('recover_one_project/',views.recover_one_project),
    path('recover_all_project/',views.recover_all_project),
    path('get_one_project/',views.get_one_project),
    path('copy/',views.copy),
    path('delete_permanently/',views.delete_permanently)
]