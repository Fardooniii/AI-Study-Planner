from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add-task/', views.add_task, name='add_task'),
    path('edit-task/<int:task_id>/', views.edit_task, name='edit_task'),
    path('delete-task/<int:task_id>/', views.delete_task, name='delete_task'),
    path('toggle-task/<int:task_id>/', views.toggle_task_complete, name='toggle_task'),
    path('add-study/', views.add_study_session, name='add_study_session'),
    path('edit-study/<int:session_id>/', views.edit_study_session, name='edit_study_session'),
    path('delete-study/<int:session_id>/', views.delete_study_session, name='delete_study_session'),
]