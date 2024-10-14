from django.contrib import admin
from django.urls import path
from projects.views import api  # Import the API instance directly

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api.urls), 
]
