from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core import serializers
from django.http import HttpResponse
from django.template import context
from django.conf import settings

from django.contrib.auth.decorators import login_required  
from django.core.exceptions import PermissionDenied        


import os 
SECRET_CODE = os.environ.get('PASSWORD')

import datetime

from main.models import Experience, Project
from main.forms import ProjectForm, ExperienceForm


def show_main(request):
    
    last_login = request.COOKIES.get('last_login', 'Belum ada sesi login / Cookie tidak ditemukan')
    context = {
        "name": "Samuel Haganta Surbakti",
        "npm": "2506612814",
        "study_program": "S1 Ilmu Komputer",
        "bio": (
            "Mahasiswa ilmu komputer di Universitas Indonesia yang tertarik pada dunia teknologi khususnya di bidang keamanan siber."
        ),
        "last_login" : last_login,
    }
    return render(request, "index.html", context)

# /////////////////////////////////////////////////////////////////
# /////////////////////////////////////////////////////////////////
#                       EXPERIENCE 
# /////////////////////////////////////////////////////////////////
# /////////////////////////////////////////////////////////////////

def show_experience(request):
    
    is_editor = request.user.groups.filter(name="Editor").exists()
    
    json_response = get_experiences_json(request)
        
    experiences = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    
    experiences = [experience.object for experience in experiences]
    
    title_query = request.GET.get("title", "").strip()
    
        
    context = {
        "name": "Samuel Haganta Surbakti",
        "experience_list": experiences,
        "title_query": title_query,
        "is_editor" : is_editor,
    }

    return render(request, "experience.html", context)

@login_required(login_url="/login/")
def create_experience(request):
    
    if not request.user.is_superuser:
        raise PermissionDenied
    
    form = ExperienceForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        
        input_code = form.cleaned_data.get("secret_code")
        
        if input_code == SECRET_CODE:
            form.save()
            messages.success(request, "Experience baru berhasil ditambahkan!")
            return redirect("main:show_experience")
        else:
            messages.error(request, "Gagal! Password salah.")
            
    context = {
        "name": "Samuel Haganta Surbakti",
        "experience_list": Experience.objects.all(),
        "form": form,
    }
    
    return render(request, "experiences_form.html", context)

def get_experiences_json(request):
    title_query = request.GET.get("title", "").strip()
    experiences = Experience.objects.all()

    if title_query:
        experiences = experiences.filter(title__icontains=title_query)

    experiences_json = serializers.serialize("json", experiences, use_natural_foreign_keys=True)
    return HttpResponse(experiences_json, content_type="application/json")


@login_required(login_url="/login/")
def delete_experience(request, experience_id):
    
    if not request.user.is_superuser:
        raise PermissionDenied
    
    experience = get_object_or_404(Experience, pk=experience_id)

    if request.method == "POST":
        experience.delete()
        messages.success(request, "Experience berhasil dihapus!")
        return redirect("main:show_experience")

    return redirect("main:show_experience")


@login_required(login_url="/login/")
def edit_experience(request, experience_id):
    
    is_editor = request.user.groups.filter(name="Editor").exists()
    if (not (is_editor or request.user.is_superuser)):
        raise PermissionDenied
    
    
    experience = get_object_or_404(Experience, pk=experience_id)
    
    form = ExperienceForm(request.POST or None, instance=experience)
    
    if form.is_valid() and request.method == "POST":
        form.save() 
        messages.success(request, "Experience berhasil diperbarui!")
        return redirect("main:show_experience")
        
    context = {
        "form": form,
        "experience": experience,
    }
    return render(request, "edit_experience.html", context)

@login_required(login_url="/login/")
def toggle_experience_star(request, experience_id):
    experience = get_object_or_404(Experience, pk=experience_id)

    if request.method == "POST":
        if request.user in experience.starred_by.all():
            experience.starred_by.remove(request.user)
        else:
            experience.starred_by.add(request.user)

    return redirect("main:show_experience")

# /////////////////////////////////////////////////////////////////
# /////////////////////////////////////////////////////////////////
#                       PROJECT 
# /////////////////////////////////////////////////////////////////
# /////////////////////////////////////////////////////////////////

def show_project(request):
    
    is_editor = request.user.groups.filter(name="Editor").exists()
    
    json_response = get_projects_json(request)
    
    projects = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    
    projects = [project.object for project in projects]
    title_query = request.GET.get("title", "").strip()
    
    context = {
        "name": "Samuel Haganta Surbakti",
        "project_list": projects,
        "title_query": title_query,
        "is_editor" : is_editor,
    }
    
    return render(request, "project.html", context)

@login_required(login_url="/login/")
def create_project(request):
    
    if not request.user.is_superuser:
        raise PermissionDenied
    
    form = ProjectForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        
        input_code = form.cleaned_data.get("secret_code")
        
        if input_code == SECRET_CODE:
            form.save()
            messages.success(request, "Proyek baru berhasil ditambahkan!")
            return redirect("main:show_project")
        else:
            messages.error(request, "Gagal! Password salah.")
            
    context = {
        "name": "Samuel Haganta Surbakti",
        "project_list": Project.objects.all(),
        "form": form,
    }
    
    return render(request, "projects_form.html", context)

def get_projects_json(request):
    title_query = request.GET.get("title", "").strip()
    projects = Project.objects.all()

    if title_query:
        projects = projects.filter(title__icontains=title_query)

    projects_json = serializers.serialize("json", projects, use_natural_foreign_keys=True)
    return HttpResponse(projects_json, content_type="application/json")


@login_required(login_url="/login/")
def delete_project(request, project_id):
    
    if not request.user.is_superuser:
        raise PermissionDenied
    
    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        project.delete()
        messages.success(request, "Project berhasil dihapus!")
        return redirect("main:show_project")

    return redirect("main:show_project")

@login_required(login_url="/login/")
def edit_project(request, project_id):
    
    is_editor = request.user.groups.filter(name="Editor").exists()
    
    if  not (is_editor or request.user.is_superuser):
        raise PermissionDenied
    
    
    project = get_object_or_404(Project, pk=project_id)
    
    form = ProjectForm(request.POST or None, instance=project)
    
    if form.is_valid() and request.method == "POST":
        form.save()
        messages.success(request, "Project berhasil diperbarui!")
        return redirect("main:show_project")
        
    context = {
        "form": form,
        "project": project,
    }
    return render(request, "edit_project.html", context)



def register(request):
    form = UserCreationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Akun berhasil dibuat. Silakan login.")
        return redirect("main:login")

    context = {
        "name": "Samuel Haganta Surbakti",
        "form": form,
    }
    return render(request, "register.html", context)


def login_user(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        login(request, form.get_user())
        response = redirect("main:show_main")
        response.set_cookie('last_login', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        return response

    context = {
        "name": "Samuel Haganta Surbakti",
        "form": form,
    }
    return render(request, "login.html", context)

def logout_user(request):
    logout(request)
    
    response = redirect("main:show_main")
    response.delete_cookie('last_login')
    return response


@login_required(login_url="/login/")
def toggle_project_star(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        if request.user in project.starred_by.all():
            project.starred_by.remove(request.user)
        else:
            project.starred_by.add(request.user)

    return redirect("main:show_project")