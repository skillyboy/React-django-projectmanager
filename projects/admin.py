from django.contrib import admin
from .models import Project

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'status', 'priority', 'assigned_to', 'created_by', 'date_created')
    fields = ('name', 'description', 'status', 'priority', 'assigned_to', 'created_by', 'date_created')  # Ensure date_created is included
    readonly_fields = ('date_created',)  # Make date_created read-only

admin.site.register(Project, ProjectAdmin)
