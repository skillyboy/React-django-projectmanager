from django import forms
from .models import Project  # Make sure you have a Project model defined

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description']  # Adjust fields based on your model
