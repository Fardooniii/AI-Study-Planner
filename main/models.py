from django.db import models
from django.contrib.auth.models import User

DIFFICULTY_CHOICES = [
    (1, 'Easy'),
    (2, 'Medium'),
    (3, 'Hard'),
    (4, 'Very Hard'),
    (5, 'Extreme')
]

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=50)
    title = models.CharField(max_length=100, default="New Task")
    difficulty = models.IntegerField(choices=DIFFICULTY_CHOICES)
    deadline = models.DateField()
    estimated_hours = models.FloatField()
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} ({self.subject})"

class StudySession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, null=True, blank=True)
    hours_studied = models.FloatField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        task_title = self.task.title if self.task else "Unassigned"
        return f"{task_title} - {self.hours_studied}h"