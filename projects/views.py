# projects/views.py

from typing import List
from ninja import Router, ModelSchema
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from .models import Project
from .forms import ProjectForm

router = Router()

# Define a Pydantic schema for your Project
class ProjectSchema(ModelSchema):
    class Config:
        model = Project
        model_fields = '__all__'  # Include all fields, adjust as necessary

# Decorator to check permissions
@router.get('/projects/', response=List[ProjectSchema])
def list_projects(request):
    request.user.is_authenticated  # Check if user is authenticated
    queryset = Project.objects.all()
    return queryset

@router.post('/projects/', response=ProjectSchema)
def create_project(request, payload: ProjectSchema):
    request.user.is_authenticated  # Check if user is authenticated
    project = Project.objects.create(**payload.dict())
    return project

@router.get('/projects/{project_id}', response=ProjectSchema)
def get_project(request, project_id: int):
    request.user.is_authenticated  # Check if user is authenticated
    project = get_object_or_404(Project, id=project_id)
    return project

@router.put('/projects/{project_id}', response=ProjectSchema)
def update_project(request, project_id: int, payload: ProjectSchema):
    request.user.is_authenticated  # Check if user is authenticated
    project = get_object_or_404(Project, id=project_id)
    for attr, value in payload.dict().items():
        setattr(project, attr, value)
    project.save()
    return project

@router.delete('/projects/{project_id}')
def delete_project(request, project_id: int):
    request.user.is_authenticated  # Check if user is authenticated
    project = get_object_or_404(Project, id=project_id)
    project.delete()
    return {"success": True}

# Add this line to your urls.py
# from projects.views import router as projects_router
# path("api/", projects_router.urls),
