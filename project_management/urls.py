# project_management/urls.py

from django.contrib import admin
from django.urls import path
from projects.views import router as projects_router

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', projects_router.urls),  # This is correct; ensure `projects_router` is from the correct import
]
