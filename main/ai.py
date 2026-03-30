from datetime import date
from .models import Task, StudySession

def calculate_task_accuracy(user):
    tasks = Task.objects.filter(user=user)
    results = []

    for task in tasks:
        sessions = StudySession.objects.filter(user=user, task=task)
        hours_done = sum(s.hours_studied for s in sessions)
        estimated = task.estimated_hours

        accuracy = round((hours_done / estimated) * 100, 2) if estimated else 0
        results.append({
            'task': task.title,
            'estimated': estimated,
            'actual': hours_done,
            'accuracy': accuracy
        })

    return results


def subject_performance(user):
    sessions = StudySession.objects.filter(user=user)
    subject_data = {}

    for session in sessions:
        if session.task:
            subject = session.task.subject
            subject_data[subject] = subject_data.get(subject, 0) + session.hours_studied

    return subject_data


def rank_tasks(user):
    tasks = Task.objects.filter(user=user, completed=False)
    today = date.today()
    ranked = []

    for task in tasks:
        sessions = StudySession.objects.filter(user=user, task=task)
        hours_done = sum(s.hours_studied for s in sessions)
        progress = (hours_done / task.estimated_hours) if task.estimated_hours else 0
        days_left = (task.deadline - today).days if task.deadline else 999

        score = (1 - progress) * 5 + (10 / (days_left + 1)) + task.difficulty
        ranked.append((score, task))

    ranked.sort(reverse=True, key=lambda x: x[0])
    return [task for score, task in ranked]


def generate_recommendations(user):
    tasks = Task.objects.filter(user=user, completed=False)
    sessions = StudySession.objects.filter(user=user)
    today = date.today()
    recommendations = []

    if not tasks:
        return ["No active tasks. Add tasks to get recommendations."]

    # top priority
    ranked = rank_tasks(user)
    if ranked:
        recommendations.append(f"Top priority: {ranked[0].title}")

    # behin schedule
    behind_tasks = []
    for task in tasks:
        task_sessions = sessions.filter(task=task)
        hours_done = sum(s.hours_studied for s in task_sessions)
        if task.estimated_hours > 0 and hours_done < task.estimated_hours:
            behind_tasks.append(task.title)
    if behind_tasks:
        if len(behind_tasks) == 1:
            recommendations.append(f"Focus on {behind_tasks[0]}, you are behind schedule")
        else:
            joined = ", ".join(behind_tasks[:-1]) + f" and {behind_tasks[-1]}"
            recommendations.append(f"Focus on {joined}, you are behind schedule")

    # not started
    not_started = [t.title for t in tasks if not sessions.filter(task=t).exists()]
    if not_started:
        if len(not_started) == 1:
            recommendations.append(f"You have not started {not_started[0]} yet")
        else:
            joined = ", ".join(not_started[:-1]) + f" and {not_started[-1]}"
            recommendations.append(f"You have not started {joined} yet")

    # daily plan
    daily_msgs = []
    for task in tasks:
        task_sessions = sessions.filter(task=task)
        hours_done = sum(s.hours_studied for s in task_sessions)
        remaining = max(task.estimated_hours - hours_done, 0)
        days_left = max((task.deadline - today).days, 1)

        if remaining > 0:
            daily_hours = max(1, round(remaining / days_left, 1))
            daily_msgs.append(f"{task.title}: {daily_hours}h/day")
    if daily_msgs:
        recommendations.append("Daily plan → " + " | ".join(daily_msgs[:3]))

    # deadlines approaching
    urgent_tasks = [t.title for t in tasks if (t.deadline - today).days <= 3]
    if urgent_tasks:
        recommendations.append("Deadlines approaching: " + ", ".join(urgent_tasks))

    # weakest subject
    subject_progress = {}
    for task in Task.objects.filter(user=user):
        subject = task.subject
        task_sessions = StudySession.objects.filter(user=user, task=task)
        hours_done = sum(s.hours_studied for s in task_sessions)
        estimated = task.estimated_hours

        if subject not in subject_progress:
            subject_progress[subject] = {'done': 0, 'estimated': 0}

        subject_progress[subject]['done'] += hours_done
        subject_progress[subject]['estimated'] += estimated

    weakest_subject = None
    lowest_progress = float('inf')
    for subject, data in subject_progress.items():
        if data['estimated'] > 0:
            progress = data['done'] / data['estimated']
            # Only consider subjects that are not fully done
            if progress < 1 and progress < lowest_progress:
                lowest_progress = progress
                weakest_subject = subject

    if weakest_subject:
        recommendations.append(f"Most behind subject: {weakest_subject}")

    return recommendations[:6]