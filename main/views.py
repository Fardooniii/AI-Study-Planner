from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from datetime import date

from .models import Task, StudySession
from .forms import TaskForm, StudySessionForm
from .ai import generate_recommendations, rank_tasks

def home(request):
    return render(request, 'main/home.html')

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'main/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'main/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def dashboard(request):
    tasks = Task.objects.filter(user=request.user).order_by('deadline')
    study_sessions = StudySession.objects.filter(user=request.user).order_by('-date')

    total_hours = sum(s.hours_studied for s in study_sessions)
    completed_tasks = tasks.filter(completed=True).count()
    total_tasks = tasks.count()

    task_progress = []
    today = date.today()
    for task in tasks:
        sessions = StudySession.objects.filter(user=request.user, task=task)
        hours_done = sum(s.hours_studied for s in sessions)
        progress = round((hours_done / task.estimated_hours) * 100, 2) if task.estimated_hours else 0
        task_progress.append({'task': task, 'hours_done': hours_done, 'percentage': progress})

    try:
        recommendations = generate_recommendations(request.user)
    except Exception:
        recommendations = ["AI temporarily unavailable"]

    smart_schedule = []
    try:
        ranked = rank_tasks(request.user)
        for task in ranked[:3]:
            sessions = StudySession.objects.filter(user=request.user, task=task)
            hours_done = sum(s.hours_studied for s in sessions)
            remaining = max(task.estimated_hours - hours_done, 0)
            days_left = max((task.deadline - today).days, 1)
            if remaining > 0:
                hours = max(1, round(remaining / days_left, 1))
                smart_schedule.append({'task': task.title, 'hours': hours})
    except Exception:
        smart_schedule = []

    warnings = []
    try:
        for task in tasks:
            sessions = StudySession.objects.filter(user=request.user, task=task)
            hours_done = sum(s.hours_studied for s in sessions)
            remaining = max(task.estimated_hours - hours_done, 0)
            days_left = (task.deadline - today).days
            if days_left > 0:
                needed_per_day = remaining / days_left
                if needed_per_day > 4:
                    warnings.append(f"{task.title}: Risk of missing deadline (need {round(needed_per_day,1)}h/day)")
    except Exception:
        warnings = []

    return render(request, 'main/dashboard.html', {
        'tasks': tasks,
        'study_sessions': study_sessions,
        'total_hours': total_hours,
        'completed_tasks': completed_tasks,
        'total_tasks': total_tasks,
        'task_progress': task_progress,
        'recommendations': recommendations,
        'smart_schedule': smart_schedule,
        'warnings': warnings
    })

@login_required
def add_task(request):
    form = TaskForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        task = form.save(commit=False)
        task.user = request.user
        task.save()
        return redirect('dashboard')
    return render(request, 'main/add_task.html', {'form': form})

@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    form = TaskForm(request.POST or None, instance=task)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('dashboard')
    return render(request, 'main/edit_task.html', {'form': form})

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.delete()
    return redirect('dashboard')

@login_required
def toggle_task_complete(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.completed = not task.completed
    task.save()
    return redirect('dashboard')

@login_required
def add_study_session(request):
    form = StudySessionForm(request.POST or None, user=request.user)
    if request.method == 'POST' and form.is_valid():
        session = form.save(commit=False)
        session.user = request.user
        session.save()
        return redirect('dashboard')
    return render(request, 'main/add_study_session.html', {'form': form})

@login_required
def edit_study_session(request, session_id):
    session = get_object_or_404(StudySession, id=session_id, user=request.user)
    form = StudySessionForm(request.POST or None, instance=session, user=request.user)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('dashboard')
    return render(request, 'main/edit_study_session.html', {'form': form})

@login_required
def delete_study_session(request, session_id):
    session = get_object_or_404(StudySession, id=session_id, user=request.user)
    session.delete()
    return redirect('dashboard')