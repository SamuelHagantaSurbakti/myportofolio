from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from main.models import Experience
from main.models import Project


# class MainTest(TestCase):
#     def setUp(self):
#         self.experience = Experience.objects.create(
#             title="Asisten Dosen PBP",
#             description="Membantu mahasiswa memahami pengembangan web.",
#             category="part-time",
#         )

#     def test_main_url_is_accessible(self):
#         response = self.client.get(reverse("main:show_main"))

#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, "index.html")
#         self.assertNotContains(response, self.experience.title)
#         self.assertContains(response, f'href="{reverse("main:show_experience")}"')

#     def test_nonexistent_page_returns_404(self):
#         response = self.client.get("/halaman-yang-tidak-ada/")

#         self.assertEqual(response.status_code, 404)

#     def test_experience_model(self):
#         self.assertEqual(str(self.experience), "Asisten Dosen PBP")
#         self.assertEqual(self.experience.category, "part-time")
#         self.assertTrue(self.experience.is_ongoing)

#     def test_experience_page(self):
#         response = self.client.get(reverse("main:show_experience"))

#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, "experience.html")
#         self.assertContains(response, self.experience.title)
#         self.assertContains(response, self.experience.description)
#         self.assertContains(response, "Part-Time")
#         self.assertContains(response, "Sedang berlangsung")
#         self.assertContains(response, f'href="{reverse("main:show_main")}"')

#     def test_empty_experience_page(self):
#         Experience.objects.all().delete()
#         response = self.client.get(reverse("main:show_experience"))

#         self.assertContains(response, "Belum ada pengalaman yang ditambahkan.")

#     def test_completed_experience(self):
#         self.experience.ended_at = timezone.now()
#         self.experience.save()
#         response = self.client.get(reverse("main:show_experience"))

#         self.assertFalse(self.experience.is_ongoing)
#         self.assertContains(response, "Selesai")
#         self.assertNotContains(response, "Sedang berlangsung")


class ProjectTest(TestCase):
    """
    project.html sekarang hanya berisi template. Data project
    dimuat lewat AJAX dari API, sehingga:
      - tes halaman HTML memeriksa kerangka + endpoint yang di-inject template,
      - permission dilakukan terhadap endpoint API.
    """

    def setUp(self):
        User = get_user_model()
        self.superuser = User.objects.create_superuser(
            username="owner", password="pass12345", email="owner@example.com"
        )
        self.user = User.objects.create_user(
            username="biasa", password="pass12345"
        )
        self.project = Project.objects.create(
            title="SamTube",
            description="Cloning aplikasi berbagi video",
            tech_stack="HTML CSS JS",
            image_url="img/SamTube.png",
            project_url="https://holysinner21.github.io/Youtube-Lawass-Cloning/",
        )

    # ---------- Halaman HTML (kerangka) ----------

    def test_url_and_template_for_projects(self):
        response = self.client.get(reverse("main:show_project"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "project.html")

    def test_project_page_is_a_shell_without_server_rendered_data(self):
        """Data project tidak lagi dirender server-side di HTML."""
        response = self.client.get(reverse("main:show_project"))

        self.assertNotContains(response, "SamTube")
        self.assertNotContains(response, "HTML CSS JS")

    def test_project_page_has_ajax_containers_and_endpoints(self):
        response = self.client.get(reverse("main:show_project"))

        self.assertContains(response, 'id="loading"')
        self.assertContains(response, 'id="error"')
        self.assertContains(response, 'id="empty"')
        self.assertContains(response, 'id="grid"')
        self.assertContains(response, "Belum ada proyek yang ditambahkan atau ditemukan.")
        self.assertContains(response, reverse("api:project-list"))

    def test_project_page_prefills_search_query(self):
        response = self.client.get(reverse("main:show_project"), {"title": "Sam"})

        self.assertContains(response, 'value="Sam"')

    def test_project_page_flags_for_anonymous(self):
        response = self.client.get(reverse("main:show_project"))

        self.assertContains(response, 'IS_SUPERUSER = "false" === "true"')
        self.assertContains(response, 'IS_AUTHENTICATED = "false" === "true"')
        self.assertNotContains(response, "Tambah Proyek")

    def test_project_page_for_superuser_shows_add_button(self):
        self.client.force_login(self.superuser)
        response = self.client.get(reverse("main:show_project"))

        self.assertContains(response, "Tambah Proyek")
        self.assertContains(response, 'IS_SUPERUSER = "true" === "true"')

    def test_project_page_for_regular_user_hides_add_button(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("main:show_project"))

        self.assertNotContains(response, "Tambah Proyek")
        self.assertContains(response, 'IS_AUTHENTICATED = "true" === "true"')

    # ---------- API: list ----------

    def test_api_project_list_with_data(self):
        response = self.client.get(reverse("api:project-list"))

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["title"], "SamTube")
        self.assertEqual(data[0]["tech_stack"], "HTML CSS JS")
        self.assertEqual(data[0]["star_count"], 0)
        self.assertFalse(data[0]["is_starred"])

    def test_api_project_list_empty_state(self):
        Project.objects.all().delete()
        response = self.client.get(reverse("api:project-list"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

    def test_api_project_list_search_by_title(self):
        Project.objects.create(
            title="Portofolio",
            description="Website pribadi",
            tech_stack="Django",
            image_url="",
            project_url="",
        )
        response = self.client.get(reverse("api:project-list"), {"title": "sam"})

        titles = [p["title"] for p in response.json()]
        self.assertEqual(titles, ["SamTube"])

    # ---------- API: create / delete (hanya superuser) ----------

    def _payload(self):
        return {
            "title": "Proyek Baru",
            "description": "Deskripsi proyek baru",
            "tech_stack": "Django",
            "project_url": "https://example.com/",
            "image_url": "gambar.jpg",
        }

    def test_api_create_project_as_superuser(self):
        self.client.force_login(self.superuser)
        response = self.client.post(
            reverse("api:project-list"), self._payload(), content_type="application/json"
        )

        self.assertEqual(response.status_code, 201)
        self.assertTrue(Project.objects.filter(title="Proyek Baru").exists())

    def test_api_create_project_forbidden_for_anonymous(self):
        response = self.client.post(
            reverse("api:project-list"), self._payload(), content_type="application/json"
        )

        self.assertIn(response.status_code, (401, 403))
        self.assertFalse(Project.objects.filter(title="Proyek Baru").exists())

    def test_api_create_project_forbidden_for_regular_user(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("api:project-list"), self._payload(), content_type="application/json"
        )

        self.assertEqual(response.status_code, 403)
        self.assertFalse(Project.objects.filter(title="Proyek Baru").exists())

    def test_api_delete_project_as_superuser(self):
        self.client.force_login(self.superuser)
        response = self.client.delete(
            reverse("api:project-detail", args=[self.project.pk])
        )

        self.assertEqual(response.status_code, 204)
        self.assertFalse(Project.objects.filter(pk=self.project.pk).exists())

    def test_api_delete_project_forbidden_for_regular_user(self):
        self.client.force_login(self.user)
        response = self.client.delete(
            reverse("api:project-detail", args=[self.project.pk])
        )

        self.assertEqual(response.status_code, 403)
        self.assertTrue(Project.objects.filter(pk=self.project.pk).exists())

    # ---------- API: star ----------

    def test_api_star_requires_login(self):
        response = self.client.post(reverse("api:project-star", args=[self.project.pk]))

        self.assertIn(response.status_code, (401, 403))
        self.assertEqual(self.project.starred_by.count(), 0)

    def test_api_star_toggle(self):
        self.client.force_login(self.user)
        url = reverse("api:project-star", args=[self.project.pk])

        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.project.starred_by.count(), 1)
        self.assertTrue(response.json()["is_starred"])
        self.assertEqual(response.json()["star_count"], 1)

        response = self.client.post(url)
        self.assertEqual(self.project.starred_by.count(), 0)
        self.assertFalse(response.json()["is_starred"])
        self.assertEqual(response.json()["star_count"], 0)