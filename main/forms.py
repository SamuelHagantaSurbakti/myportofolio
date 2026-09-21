from django.forms import ModelForm, TextInput, Textarea, URLInput, CharField, PasswordInput, Select, DateInput

from main.models import Project, Experience

class ProjectForm(ModelForm):
    
    secret_code = CharField(
        label="Password",
        required=True,
        widget=PasswordInput(
            attrs={
                "placeholder": "Masukkann Password",
                "class": "project-form__input", 
                "autocomplete": "new-password",
            }
        )
    )
    
    class Meta:
        model = Project
        fields = [
            "title",
            "description",
            "tech_stack",
            "project_link",
            "image_url",
        ]

        labels = {
            "title": "Nama Proyek",
            "description": "Deskripsi Proyek",
            "tech_stack": "Teknologi yang Digunakan",
            "project_link": "URL Proyek",
            "image_url": "URL Gambar Proyek",
        }
        
        

        widgets = {
            "title": TextInput(
                attrs={
                    "placeholder": "Portfolio Website",
                    "maxlength": 255,
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Ceritakan Proyekmu",
                    "rows": 3,
                }
            ),
            "tech_stack": TextInput(
                attrs={
                    "placeholder": "Django, Python, HTML, CSS",
                }
            ),
            "project_link": URLInput(
                attrs={
                    "placeholder": "https://github.com/kakBurhan/burhanquestv4",
                }
            ),
            "image_url": URLInput(
                attrs={
                    "placeholder": "https://drive.google.com/thumbnail?id=...&sz=w1000",
                }
            ),
        }
        
    
class ExperienceForm(ModelForm):
    secret_code = CharField(
        label="Password",
        required=True,
        widget=PasswordInput(
            attrs={
                "placeholder": "Masukkan Password",
                "class": "experience-form__input", 
                "autocomplete": "new-password",
            }
        )
    )
    
    class Meta:
        model = Experience
        fields = [
            "title",
            "description",
            "category",
            "thumbnail",
            "started_at",
            "ended_at",
        ]

        labels = {
            "title": "Nama Experience",
            "description": "Deskripsi Experience",
            "category": "Kategori Experience",
            "thumbnail": "URL Thumbnail Experience (16 : 9)",
            "started_at": "Tanggal Dimulai",
            "ended_at": "Tanggal Selesai",
        }

        widgets = {
            "title": TextInput(
                attrs={
                    "placeholder": "Contoh: Software Engineer Intern",
                    "maxlength": 255,
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Ceritakan peran dan kontribusimu...",
                    "rows": 3,
                }
            ),
            "category": Select( 
                attrs={
                    "class": "experience-form__select", 
                }
            ),
            "thumbnail": URLInput( 
                attrs={
                    "placeholder": "https://drive.google.com/thumbnail?id=...&sz=w1000",
                }
            ),
            "started_at": DateInput( 
                attrs={
                    "type": "date"
                }
            ),
            "ended_at": DateInput(
                attrs={
                    "type": "date", 
                }
            ),
        }