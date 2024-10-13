# urls.py

from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import *

urlpatterns = [
    
    # path('api-token-auth/', obtain_auth_token, name='api-token-auth'),  # Token authentication
    # path('projects/', ProjectListView.as_view(), name='project-list'),  # List and create projects
    # path('projects/<int:pk>/', ProjectDetailView.as_view(), name='project-detail'),  # Retrieve, update, delete project
]
