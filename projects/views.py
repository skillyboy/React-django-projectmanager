from typing import List
from ninja import NinjaAPI, ModelSchema, Field
from django.shortcuts import get_object_or_404
from .models import Project
from django.contrib.auth.models import User
import logging
from ninja.errors import HttpError
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from ninja import Schema
logger = logging.getLogger(__name__)

# Create the API instance
api = NinjaAPI()





class LoginSchema(Schema):
    username: str
    password: str

@api.post('/login/')
def login_user(request, payload: LoginSchema):
    user = authenticate(request, username=payload.username, password=payload.password)
    if user is not None:
        login(request, user)
        return {"success": True}
    else:
        raise HttpError(401, {"error": "Invalid credentials"})


class ProjectSchema(ModelSchema):
    created_by: str = Field(..., exclude=True)  # Exclude from input

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
            assigned_to=project.assigned_to,
            created_by=str(project.created_by)  # Convert User to string (e.g., username)
        )

# Permission check decorator for authenticated users
def is_authenticated(request):
    if not request.user.is_authenticated:
        logger.warning("Unauthorized access attempt.")
        raise HttpError(401, {"error": "Unauthorized"})  # Raise an exception instead of returning a dict

# Permission check decorator for admin users
def is_admin(request):
    if not request.user.is_staff:
        logger.warning("Forbidden access attempt by non-admin user.")
        raise HttpError(403, {"error": "Forbidden"})  # Raise an exception instead of returning a dict

@api.get('/projects/', response=List[ProjectSchema])
def list_projects(request):
    is_authenticated(request)  # Check authentication

    queryset = Project.objects.all() if request.user.is_staff else Project.objects.filter(assigned_to=request.user)
    projects = [ProjectSchema.from_model(project) for project in queryset]

    # Ensure the returned projects are correctly serialized
    serialized_projects = [
        {
            "id": project.id,
            "name": project.name,
            "description": project.description,
            "created_by": str(project.created_by),  # Convert to string if necessary
        }
        for project in projects
    ]

    return serialized_projects

@api.post('/projects/', response=ProjectSchema)
def create_project(request, payload: ProjectSchema):
    is_authenticated(request)  # Check authentication

    assigned_to_user = get_object_or_404(User, id=payload.assigned_to.id)

    project_data = payload.dict(exclude={"created_by", "assigned_to"})
    project = Project.objects.create(**project_data, created_by=request.user, assigned_to=assigned_to_user)

    logger.info(f"Project created: {project}")
    return ProjectSchema.from_model(project)  # Return the created project as a schema

@api.get('/projects/{project_id}/', response=ProjectSchema)
def get_project(request, project_id: int):
    is_authenticated(request)  # Check authentication

    project = get_object_or_404(Project, id=project_id)

    if not request.user.is_staff and project.assigned_to != request.user:
        raise HttpError(403, {"error": "Forbidden"})  # Raise an exception for forbidden access

    return ProjectSchema.from_model(project)

@api.put('/projects/{project_id}/', response=ProjectSchema)
def update_project(request, project_id: int, payload: ProjectSchema):
    is_admin(request)  # Check admin permissions

    project = get_object_or_404(Project, id=project_id)

    for attr, value in payload.dict().items():
        if attr == "assigned_to":
            assigned_to_user = get_object_or_404(User, id=value)
            setattr(project, attr, assigned_to_user)
        else:
            setattr(project, attr, value)

    project.save()
    logger.info(f"Project updated: {project}")
    return ProjectSchema.from_model(project)  # Return the updated project

@api.delete('/projects/{project_id}/')
def delete_project(request, project_id: int):
    is_admin(request)  # Check admin permissions

    project = get_object_or_404(Project, id=project_id)
    project.delete()
    logger.info(f"Project deleted: {project_id}")
    return {"success": True}  # This response is valid
