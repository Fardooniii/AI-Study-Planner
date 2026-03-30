from django import forms
from datetime import date
from .models import Task, StudySession


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'subject', 'difficulty', 'deadline', 'estimated_hours']

    def clean_deadline(self):
        deadline = self.cleaned_data.get('deadline')

        if deadline and deadline < date.today():
            raise forms.ValidationError("Deadline cannot be in the past")

        return deadline

    def clean_estimated_hours(self):
        hours = self.cleaned_data.get('estimated_hours')

        if hours is not None and hours <= 0:
            raise forms.ValidationError("Estimated hours must be greater than 0")

        return hours


class StudySessionForm(forms.ModelForm):
    class Meta:
        model = StudySession
        fields = ['task', 'hours_studied']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user:
            self.fields['task'].queryset = Task.objects.filter(user=user)

    def clean_hours_studied(self):
        hours = self.cleaned_data.get('hours_studied')

        if hours is not None and hours <= 0:
            raise forms.ValidationError("Study hours must be greater than 0")

        return hours