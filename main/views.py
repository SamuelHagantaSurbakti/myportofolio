from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core import serializers
from django.http import HttpResponse
from django.template import context
from django.conf import settings
from django.http import JsonResponse
import json


from django.contrib.auth.decorators import login_required  
from django.core.exceptions import PermissionDenied       
from django.views.decorators.http import require_POST 


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
    title_query = request.GET.get("title", "").strip()
    is_editor = request.user.groups.filter(name='Editor').exists()
    
    context = {
        "name": "Samuel Haganta Surbakti",
        "title_query" : title_query,
        "is_editor" : is_editor,
        "form": ExperienceForm(),
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
    experiences = Experience.objects.prefetch_related('starred_by').all()

    if title_query:
        experiences = experiences.filter(title__icontains=title_query)
        
    data = []
    for experience in experiences:
        
        starred_users = experience.starred_by.all()
        is_starred = request.user in starred_users if request.user.is_authenticated else False
        starred_by_names = ", ".join([u.username for u in starred_users])
        
        data.append({
            "pk" : str(experience.id),
            "fields" : {
                "title" : experience.title,
                "description" : experience.description,
                "category" : experience.category,
                "thumbnail" : experience.thumbnail,
                "started_at" : experience.started_at,
                "ended_at" : experience.ended_at,
                "is_ongoing" : experience.is_ongoing,
                
                "star_count": starred_users.count(),
                "is_starred": is_starred,
                "starred_by_names": starred_by_names,
            }
        })
        
    return JsonResponse(data, safe=False)


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


@require_POST
def create_experience_ajax(request):
    if not request.user.is_superuser:
        return JsonResponse(
            {"message": "Hanya pemilik portofolio yang dapat menambahkan experience."},
            status=403,
        )

    form = ExperienceForm(request.POST)
    if form.is_valid():
        if form.cleaned_data.get("secret_code") != SECRET_CODE:
            return JsonResponse({"message": "Password salah."}, status=403)

        experience = form.save()
        return JsonResponse(
            {"message": "Experience berhasil ditambahkan.", "pk": str(experience.id)},
            status=201,
        )

    return JsonResponse({"errors": form.errors.get_json_data()}, status=400)

# /////////////////////////////////////////////////////////////////
# /////////////////////////////////////////////////////////////////
#                       PROJECT 
# /////////////////////////////////////////////////////////////////
# /////////////////////////////////////////////////////////////////

def show_project(request):
    
    is_editor = request.user.groups.filter(name="Editor").exists()
    title_query = request.GET.get("title", "").strip()
    
    context = {
        "name": "Samuel Haganta Surbakti",
        "title_query": title_query,
        "is_editor" : is_editor,
        "form": ProjectForm(),
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
    projects = Project.objects.prefetch_related('starred_by').all()

    if title_query:
        projects = projects.filter(title__icontains=title_query)
    
    data = []
    for project in projects:
        
        starred_users = project.starred_by.all()
        is_starred = request.user in starred_users if request.user.is_authenticated else False
        starred_by_names = ", ".join([u.username for u in starred_users])

        data.append({
            "pk": str(project.pk),
            "fields": {
                "title": project.title,
                "description": project.description,
                "tech_stack": project.tech_stack,
                "project_link": project.project_link,
                "image_url": project.image_url,
                
                "star_count": starred_users.count(),
                "is_starred": is_starred,
                "starred_by_names": starred_by_names,
            }
        })

    return JsonResponse(data, safe=False)


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

@require_POST
def create_project_ajax(request):
    if not request.user.is_superuser:
        return JsonResponse(
            {"message": "Hanya pemilik portofolio yang dapat menambahkan proyek."},
            status=403,
        )

    form = ProjectForm(request.POST)
    if form.is_valid():
        project = form.save()
        return JsonResponse(
            {"message": "Proyek berhasil ditambahkan.", "pk": str(project.id)},
            status=201,
        )

    return JsonResponse({"errors": form.errors.get_json_data()}, status=400)

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