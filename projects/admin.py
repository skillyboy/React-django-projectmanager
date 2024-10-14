from django.contrib import admin
from .models import Project

# Register your models here.
# Register the model and the custom admin class
admin.site.register(Project,)