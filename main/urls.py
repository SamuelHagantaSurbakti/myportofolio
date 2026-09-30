from venv import create

from django.urls import path

from main.views import show_main
from main.views import show_project, create_project, get_projects_json,   delete_project, edit_project, create_project_ajax
from main.views import show_experience, create_experience, get_experiences_json, delete_experience, edit_experience
from main.views import register, login_user, logout_user
from main.views import toggle_project_star, toggle_experience_star

app_name = "main"

urlpatterns = [ 
    path("", show_main, name="show_main"),
    
    path("experience/", show_experience, name="show_experience"),
    path("experience/edit", edit_project, name="edit_project"),
    path("experience/add/", create_experience, name="create_experience"),
    path("api/experiences/", get_experiences_json, name="get_experiences_json"),
    path("experience/<uuid:experience_id>/delete/",delete_experience,name="delete_experience"),
    path('experience/edit/<uuid:experience_id>/', edit_experience, name='edit_experience'),
    
    path("project/", show_project, name="show_project"),
    path("project/add/", create_project, name="create_project"),
    path("project/edit/", edit_experience, name="edit_experience"),
    path("api/projects/", get_projects_json, name="get_projects_json"),
    path("projects/<uuid:project_id>/delete/",delete_project,name="delete_project"),
    path('project/edit/<uuid:project_id>/', edit_project, name='edit_project'),
    path("projects/add-ajax/", create_project_ajax, name="create_project_ajax"),
    
    
    path("register/", register, name="register"),
    path("login/", login_user, name="login"),
    path("logout/", logout_user, name="logout"),
    
    path("projects/<uuid:project_id>/star/", toggle_project_star, name="toggle_project_star"),
    path("experiences/<uuid:experience_id>/star/", toggle_experience_star, name="toggle_experience_star"),
]
