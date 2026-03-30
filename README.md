# AI-Powered Study Planner (Django Web Application)

## Overview
This project is a full-stack web application built using Django that helps students manage their academic workload through task tracking, study session logging, and intelligent analytics. The system combines structured data management with algorithmic recommendations to improve productivity and study efficiency.

## Features

### User Authentication
- Secure signup, login, and logout using Django’s built-in authentication system
- Personalized user dashboard with private data

### Task Management
- Create, edit, delete, and mark tasks as completed
- Each task includes:
  - Subject
  - Title
  - Difficulty level (1–5)
  - Deadline
  - Estimated study hours
- Tasks are automatically sorted by deadline

### Study Session tracking
- Log daily study sessions linked to tasks
- Track hours studied and study date
- Compare planned vs actual effort

### Progress Monitoring
- Calculates completion percentage based on logged vs estimated hours
- Displays progress indicators for each task
- Shows total study time and overall statistics

### AI Features

#### Task Priority ranking
- Ranks tasks dynamically based on:
  - Remaining work
  - Deadline proximity
  - Task difficulty

#### Intelligent recommendations
- Identifies:
  - Tasks behind schedule
  - Tasks not yet started
  - Urgent deadlines
- Groups insights to avoid clutter

#### Smart daily study plan
- Calculates required study hours per task per day
- Based on remaining work and time left
- Enforces a minimum of 1 hour per day
- Displays top 3 priority tasks

#### Deadline risk prediction
- Detects tasks at risk of missing deadlines
- Warns when required daily study exceeds a threshold

#### Subject performance analysis
- Analyzes performance across subjects
- Identifies weakest subject based on completion ratio
- Handles edge cases to avoid misleading results

## Technical stack
- Backend: Django (Python)
- Database: SQLite (default Django database)
- Architecture:
  - Models: Task, StudySession
  - Views: request handling and logic
  - Templates: dynamic UI rendering
  - ai.py: modular AI and analytics logic

## Key concepts
- Object-Relational Mapping (ORM)
- Query filtering and aggregation
- Algorithmic scoring systems
- Data analysis and transformation
- Error handling and edge cases

## installation

1. Clone the repository:
   git clone <your-repo-url>

2. Navigate into the project folder:
   cd <project-folder>

3. Create a virtual environment:
   python -m venv venv

4. Activate the virtual environment:
   Windows:
   venv\Scripts\activate

   Mac/Linux:
   source venv/bin/activate

5. Install dependencies:
   pip install -r requirements.txt

6. Run migrations:
   python manage.py migrate

7. Start the development server:
   python manage.py runserver

8. Open in browser:
   http://127.0.0.1:8000/

## future Improvement
- Integration of machine learning models for predictive analysis
- Deployment (e.g., Heroku, Render)
- Improved UI/UX design
- REST API support
