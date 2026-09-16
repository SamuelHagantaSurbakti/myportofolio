from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.template import context

from main.models import Experience, Project
from main.forms import ProjectForm


def show_main(request):
    context = {
        "name": "Samuel Haganta Surbakti",
        "npm": "2506612814",
        "study_program": "S1 Ilmu Komputer",
        "bio": (
            "Mahasiswa Ilmu Komputer Universitas Indonesia yang tertarik "
            "pada pengembangan perangkat lunak dan pendidikan."
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
    context = {
        "name": "Samuel Haganta Surbakti",
        "project_list": Project.objects.all(),
    }
    
    return render(request, "project.html", context)


def create_project(request):
    form = ProjectForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Proyek baru berhasil ditambahkan!")
        return redirect("main:show_project")

    context = {
        "name": "Samuel Haganta Surbakti",
        "project_list": Project.objects.all(),
    }
    
    return render(request, "projects_form.html", context)