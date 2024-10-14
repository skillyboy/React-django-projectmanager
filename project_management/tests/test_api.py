import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from ninja import NinjaAPI
from .models import Project

User = get_user_model()
api = NinjaAPI()

@pytest.fixture
def user(db):
    return User.objects.create_user(username='testuser', password='testpassword')

@pytest.fixture
def client():
    from rest_framework.test import APIClient
    return APIClient()

@pytest.fixture
def project(db, user):
    return Project.objects.create(
        name="Test Project",
        description="Test Description",
        status="ongoing",
        priority="high",
        created_by=user,
        assigned_to=user
    )

# Test for user login
def test_login_user(client, user):
    response = client.post(reverse('login_user'), {'username': 'testuser', 'password': 'testpassword'})
    assert response.status_code == status.HTTP_200_OK
    assert response.data == {"success": True}

def test_login_invalid_user(client):
    response = client.post(reverse('login_user'), {'username': 'wronguser', 'password': 'wrongpassword'})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.data == {"error": "Invalid credentials"}

# Test for listing projects
def test_list_projects(client, user, project):
    client.login(username='testuser', password='testpassword')
    response = client.get(reverse('list_projects'))
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]['name'] == "Test Project"

# Test for creating a project
def test_create_project(client, user):
    client.login(username='testuser', password='testpassword')
    response = client.post(reverse('create_project'), {
        'name': "New Project",
        'description': "New Project Description",
        'status': "ongoing",
        'priority': "medium",
        'assigned_to': user.id,
    })
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['name'] == "New Project"

# Test for getting a project
def test_get_project(client, user, project):
    client.login(username='testuser', password='testpassword')
    response = client.get(reverse('get_project', args=[project.id]))
    assert response.status_code == status.HTTP_200_OK
    assert response.data['name'] == project.name

# Test for updating a project
def test_update_project(client, user, project):
    client.login(username='testuser', password='testpassword')
    response = client.put(reverse('update_project', args=[project.id]), {
        'name': "Updated Project",
        'description': "Updated Description",
        'status': "completed",
        'priority': "low",
        'assigned_to': user.id,
    })
    assert response.status_code == status.HTTP_200_OK
    assert response.data['name'] == "Updated Project"

# Test for deleting a project
def test_delete_project(client, user, project):
    client.login(username='testuser', password='testpassword')
    response = client.delete(reverse('delete_project', args=[project.id]))
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Project.objects.filter(id=project.id).count() == 0
