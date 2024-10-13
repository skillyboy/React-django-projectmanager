from typing import List
from ninja import NinjaAPI, ModelSchema
from django.shortcuts import get_object_or_404
from .models import Project
from ninja import Schema, Field

# Create the API instance
api = NinjaAPI()

# Define a Pydantic schema for your Project
class ProjectSchema(ModelSchema):
    class Config:
        model = Project
        model_fields = '__all__'  # Include all fields, adjust as necessary

# Decorator to check permissions
def is_authenticated(request):
    if not request.user.is_authenticated:
        return {"error": "Unauthorized"}, 401

@api.get('/projects/', response=List[ProjectSchema])
def list_projects(request):
    auth_response = is_authenticated(request)
    if auth_response:
        return auth_response  # Return error if unauthorized
    queryset = Project.objects.all()
    return queryset

@api.post('/projects/', response=ProjectSchema)
def create_project(request, payload: ProjectSchema):
    auth_response = is_authenticated(request)
    if auth_response:
        return auth_response  # Return error if unauthorized
    project = Project.objects.create(**payload.dict(), created_by=request.user)  # Assuming `created_by` is a field
    return project

@api.get('/projects/{project_id}', response=ProjectSchema)
def get_project(request, project_id: int):
    auth_response = is_authenticated(request)
    if auth_response:
        return auth_response  # Return error if unauthorized
    project = get_object_or_404(Project, id=project_id)
    return project

@api.put('/projects/{project_id}', response=ProjectSchema)
def update_project(request, project_id: int, payload: ProjectSchema):
    auth_response = is_authenticated(request)
    if auth_response:
        return auth_response  # Return error if unauthorized
    project = get_object_or_404(Project, id=project_id)
    for attr, value in payload.dict().items():
        setattr(project, attr, value)
    project.save()
    return project

@api.delete('/projects/{project_id}')
def delete_project(request, project_id: int):
    auth_response = is_authenticated(request)
    if auth_response:
        return auth_response  # Return error if unauthorized
    project = get_object_or_404(Project, id=project_id)
    project.delete()
    return {"success": True}
