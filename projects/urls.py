from django.urls import path
from .api import api  # Assuming your API is in api.py

urlpatterns = [
    path('api/', api.urls),
]
