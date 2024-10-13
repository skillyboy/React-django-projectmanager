from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Project
from django.contrib.auth.models import User

class ProjectTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.admin_user = User.objects.create_superuser(username='admin', password='adminpass')
        self.client.login(username='testuser', password='testpass')

    def test_create_project(self):
        url = reverse('project-list')
        data = {'name': 'Test Project', 'description': 'Test description', 'assigned_to': self.user.id, 'created_by': self.user.id, 'status': 'in_progress', 'priority': 'low'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  # Regular user shouldn't be able to create

        self.client.login(username='admin', password='adminpass')  # Log in as admin
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
