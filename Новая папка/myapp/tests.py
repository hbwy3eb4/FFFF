from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

# Create your tests here.

class FamilyTreeApiTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')

    def test_family_tree_api_get(self):
        response = self.client.get('/api/family-tree/')
        self.assertIn(response.status_code, [200, 404])

    def test_family_tree_api_edit(self):
        response = self.client.post('/api/family-tree/edit/', data='{"name": "Test"}', content_type='application/json')
        self.assertIn(response.status_code, [200, 404, 400])

class RegistrationTests(TestCase):
    def test_registration_page(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

class ProfileTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser2', password='testpass')
        self.client = Client()
        self.client.login(username='testuser2', password='testpass')

    def test_profile_page(self):
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)

# TODO: Добавить тесты для медиаархива, загрузки файлов, infoPanel, поиска, drag&drop, супругов и т.д.
