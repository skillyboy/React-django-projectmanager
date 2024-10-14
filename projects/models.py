from django.contrib.auth.models import User
from django.db import models

class Project(models.Model):
    STATUS_CHOICES = [
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
        ('abandoned', 'Abandoned'),
        ('canceled', 'Canceled'),
    ]

    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('mid', 'Mid'),
        ('high', 'High'),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField()
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='projects_created', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_progress')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='low')
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
