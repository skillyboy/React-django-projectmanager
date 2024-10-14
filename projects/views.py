from typing import List
from ninja import NinjaAPI, ModelSchema, Field
from django.shortcuts import get_object_or_404
from ninja.errors import HttpError  # Correct import for HttpError

from .models import Project
from django.contrib.auth.models import User
import logging

# Set up logging
logger = logging.getLogger(__name__)

# Create NinjaAPI instance
api = NinjaAPI()

# Project schema for serialization
class ProjectSchema(ModelSchema):
    created_by: str = Field(..., exclude=True)  # Exclude `created_by` from input

    class Config:
        model = Project
        model_fields = '__all__'

    @classmethod
    def from_model(cls, project: Project) -> 'ProjectSchema':
        """Convert a Project instance to ProjectSchema, handling created_by correctly."""
        return cls(
            id=project.id,
            name=project.name,
            description=project.description,
            status=project.status,
            priority=project.priority,
            date_created=project.date_created,
            assigned_to=project.assigned_to.id,  # Use ID for assigned_to in response
            created_by=str(project.created_by)   # Convert User to string (e.g., username)
        )

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

# Create a new project (admin-only access)
@api.post('/projects/', response=ProjectSchema)
def create_project(request, payload: ProjectSchema):
    # Validate status and priority
    valid_statuses = ['in_progress', 'done', 'abandoned', 'canceled']
    valid_priorities = ['low', 'mid', 'high']

    if payload.status not in valid_statuses:
        raise HttpError(400, f"Invalid status: {payload.status}")
    
    if payload.priority not in valid_priorities:
        raise HttpError(400, f"Invalid priority: {payload.priority}")

    assigned_to_user = get_object_or_404(User, id=payload.assigned_to)
    project_data = payload.dict(exclude={"created_by", "assigned_to"})
    project = Project.objects.create(**project_data, created_by=request.user, assigned_to=assigned_to_user)

    logger.info(f"Project created: {project}")
    return ProjectSchema.from_model(project)

# Update an existing project (admin-only access)
@api.put('/projects/{project_id}/', response=ProjectSchema)
def update_project(request, project_id: int, payload: ProjectSchema):
    is_admin(request)  # Check admin permissions
    project = get_object_or_404(Project, id=project_id)

    # Validate status and priority
    valid_statuses = ['in_progress', 'done', 'abandoned', 'canceled']
    valid_priorities = ['low', 'mid', 'high']

    if payload.status not in valid_statuses:
        raise HttpError(400, f"Invalid status: {payload.status}")

    if payload.priority not in valid_priorities:
        raise HttpError(400, f"Invalid priority: {payload.priority}")

    # Update the project fields
    for attr, value in payload.dict().items():
        if attr == "assigned_to":
            assigned_to_user = get_object_or_404(User, id=value)
            setattr(project, attr, assigned_to_user)
        else:
            setattr(project, attr, value)

    project.save()
    logger.info(f"Project updated: {project}")
    return ProjectSchema.from_model(project)

# Retrieve a specific project (authenticated users)
@api.get('/projects/{project_id}/', response=ProjectSchema)
def get_project(request, project_id: int):
    auth_response = is_authenticated(request)
    if auth_response:
        return auth_response

    project = get_object_or_404(Project, id=project_id)

    # Allow project access if user is admin or assigned to the project
    if not request.user.is_staff and project.assigned_to != request.user:
        return {"error": "Forbidden"}, 403

    return ProjectSchema.from_model(project)

# Delete a project (admin-only access)
@api.delete('/projects/{project_id}/')
def delete_project(request, project_id: int):
    auth_response = is_admin(request)
    if auth_response:
        return auth_response

    project = get_object_or_404(Project, id=project_id)
    project.delete()
    logger.info(f"Project deleted: {project_id}")
    return {"success": True}
