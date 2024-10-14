
# Project Management App

This Project Management App allows users to create, manage, and track projects. It includes both backend API implementations using Django and a frontend built with React. The app supports different user roles (Admin and User) and includes functionality to handle project attributes and permissions.

## Features

- **User Roles**:
  - **Admin**: Can create, update, delete projects, and assign users.
  - **User**: Can view projects assigned to them.

- **Project Attributes**:
  - **Status**: Projects can be marked as "In Progress", "Done", "Abandoned", or "Canceled".
  - **Priority**: Projects can be assigned a priority of "Low", "Medium", or "High".
  - **Name**: Title of the project.
  - **Description**: Brief details about the project.
  - **Assigned To**: User ID of the assigned team member.
  - **Created By**: User ID of the admin who created the project.
  - **Date Created**: Timestamp when the project was created.

## API Implementation

The backend API is built using Django, with endpoints for CRUD operations on projects. It uses Django's built-in user authentication for secure access. The `Project` model is defined with necessary attributes, and permissions are enforced based on user roles.

### Model Definition

```python
from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
    STATUS_CHOICES = [
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
        ('abandoned', 'Abandoned'),
        ('canceled', 'Canceled'),
    ]
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('mid', 'Medium'),
        ('high', 'High'),
    ]
    name = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='in_progress')
    priority = models.CharField(max_length=15, choices=PRIORITY_CHOICES, default='low')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='projects')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_projects')
    date_created = models.DateTimeField(auto_now_add=True)
```

### Admin Interface

Django’s built-in admin UI is utilized to manage projects effectively. A custom admin class enhances the interface by defining which fields to display, adding search and filtering options, and enforcing permissions.

```python
from django.contrib import admin
from .models import Project

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'priority', 'assigned_to', 'created_by', 'date_created')
    list_filter = ('status', 'priority', 'assigned_to')
    search_fields = ('name', 'description', 'assigned_to__username')
    list_editable = ('status', 'priority')

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_add_permission(self, request):
        return request.user.is_superuser

admin.site.register(Project, ProjectAdmin)
```

## Frontend Implementation

The frontend is built with React, providing a user-friendly interface for project management. It includes forms for project creation and lists projects with their attributes. The app handles input validation and error messaging effectively.

### Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. **Set up the backend**:
   - Navigate to the backend folder and install requirements:
     ```bash
     pip install -r requirements.txt
     ```
   - Run migrations:
     ```bash
     python manage.py migrate
     ```
   - Create a superuser:
     ```bash
     python manage.py createsuperuser
     ```
   - Start the server:
     ```bash
     python manage.py runserver
     ```

3. **Set up the frontend**:
   - Navigate to the frontend folder and install dependencies:
     ```bash
     npm install
     ```
   - Start the frontend:
     ```bash
     npm start
     ```

## Conclusion

This Project Management App provides a robust solution for managing projects, leveraging Django's powerful features for the backend and a responsive React frontend. Feel free to customize and extend the functionalities as needed.
```

### Explanation of the README

- **Project Overview**: It provides a brief introduction and key features of the app.
- **API Implementation**: It includes the model definition and admin interface customization.
- **Frontend Implementation**: Instructions are given on how to set up both the backend and frontend environments.
- **Conclusion**: A summary of the app's capabilities and encouragement for further customization.

You can modify the repository URL and other specifics based on your actual project setup.