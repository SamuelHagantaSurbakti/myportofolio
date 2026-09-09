from django.shortcuts import render
from main.models import Experience


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
