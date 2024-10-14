from typing import List
from ninja import NinjaAPI, ModelSchema, Field
from django.shortcuts import get_object_or_404
from .models import Project
from django.contrib.auth.models import User
import logging

logger = logging.getLogger(__name__)

# Create the API instance
api = NinjaAPI()

class ProjectSchema(ModelSchema):
    class Config:
        model = Project
        model_fields = '__all__'  # This includes all fields

    created_by: str = Field(..., exclude=True)  # Exclude created_by field from input


# Permission check decorator for authenticated users
def is_authenticated(request):
    if not request.user.is_authenticated:
        logger.warning("Unauthorized access attempt.")
        return {"error": "Unauthorized"}, 401


# Permission check decorator for admin users
def is_admin(request):
    if not request.user.is_staff:
        logger.warning("Forbidden access attempt by non-admin user.")
        return {"error": "Forbidden"}, 403


@api.get('/projects/', response=List[ProjectSchema])
def list_projects(request):
    auth_response = is_authenticated(request)
    if auth_response:
        return auth_response  # Return error if unauthorized

    queryset = Project.objects.all() if request.user.is_staff else Project.objects.filter(assigned_to=request.user)
    return queryset


@api.post('/projects/', response=ProjectSchema)
def create_project(request, payload: ProjectSchema):
    auth_response = is_authenticated(request)
    if auth_response:
        return auth_response  # Return error if unauthorized

    assigned_to_user = get_object_or_404(User, id=payload.assigned_to.id)

    project_data = payload.dict(exclude={"created_by", "assigned_to"})
    project = Project.objects.create(**project_data, created_by=request.user, assigned_to=assigned_to_user)

    logger.info(f"Project created: {project}")
    return project


@api.get('/projects/{project_id}/', response=ProjectSchema)
def get_project(request, project_id: int):
    auth_response = is_authenticated(request)
    if auth_response:
        return auth_response  # Return error if unauthorized

    logger.debug(f"Attempting to retrieve project with ID: {project_id}")
    project = get_object_or_404(Project, id=project_id)

    if not request.user.is_staff and project.assigned_to != request.user:
        logger.warning(f"User {request.user} tried to access a forbidden project with ID: {project_id}.")
        return {"error": "Forbidden"}, 403

    logger.debug(f"Project found: {project}")
    return project


@api.put('/projects/{project_id}/', response=ProjectSchema)
def update_project(request, project_id: int, payload: ProjectSchema):
    auth_response = is_admin(request)
    if auth_response:
        return auth_response  # Return error if not authorized to update

    project = get_object_or_404(Project, id=project_id)

    for attr, value in payload.dict().items():
        if attr == "assigned_to":
            assigned_to_user = get_object_or_404(User, id=value)
            setattr(project, attr, assigned_to_user)
        else:
            setattr(project, attr, value)

    project.save()
    logger.info(f"Project updated: {project}")
    return project


@api.delete('/projects/{project_id}/')
def delete_project(request, project_id: int):
    auth_response = is_admin(request)
    if auth_response:
        return auth_response  # Return error if not authorized to delete

    project = get_object_or_404(Project, id=project_id)
    project.delete()
    logger.info(f"Project deleted: {project_id}")
    return {"success": True}
