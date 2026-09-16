from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.template import context
from django.conf import settings

from main.models import Experience, Project
from main.forms import ProjectForm


def show_main(request):
    context = {
        "name": "Samuel Haganta Surbakti",
        "npm": "2506612814",
        "study_program": "S1 Ilmu Komputer",
        "bio": (
            "Mahasiswa ilmu komputer di Universitas Indonesia yang tertarik pada dunia teknologi khususnya di bidang keamanan siber."
        ),
    }
    return render(request, "index.html", context)


def show_experience(request):
    context = {
        "name": "Samuel Haganta Surbakti",
        "experience_list": Experience.objects.all(),
    }

    return render(request, "experience.html", context)

def show_project(request):
    
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
    }
    
    return render(request, "project.html", context)


def create_project(request):
    form = ProjectForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        
        input_code = form.cleaned_data.get("secret_code")
        
        if input_code == settings.SECRET_CODE:
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

    projects_json = serializers.serialize("json", projects)
    return HttpResponse(projects_json, content_type="application/json")

def delete_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        project.delete()
        messages.success(request, "Project berhasil dihapus!")
        return redirect("main:show_project")

    return redirect("main:show_project")