# admin.py
from django.contrib import admin
from .models import Project

class ProjectAdmin(admin.ModelAdmin):
    # Specify the fields to be displayed in the list view
    list_display = ('name', 'status', 'priority', 'assigned_to', 'created_by', 'date_created')
    
    # Add filters to the admin sidebar
    list_filter = ('status', 'priority', 'assigned_to')
    
    # Add search functionality
    search_fields = ('name', 'description', 'assigned_to__username')  # assuming 'assigned_to' is a User model
    
    # Make fields editable directly from the list view
    list_editable = ('status', 'priority')

    # Specify fields to display in the detail view
    fields = ('name', 'description', 'status', 'priority', 'assigned_to', 'created_by', 'date_created')
    
    # Ensure only admins can create, update, or delete projects
    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser  # Only superusers (admins) can change projects

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser  # Only superusers can delete projects

    def has_add_permission(self, request):
        return request.user.is_superuser  # Only superusers can add projects

# Register the model and the custom admin class
admin.site.register(Project, ProjectAdmin)
