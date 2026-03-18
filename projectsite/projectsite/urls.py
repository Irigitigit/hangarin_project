"""
URL configuration for projectsite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from tasks import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.TaskListView.as_view(), name='home'),
    
    # Task URLs
    path('tasks/create/', views.TaskCreateView.as_view(), name='task_create'),
    path('tasks/<int:pk>/update/', views.TaskUpdateView.as_view(), name='task_update'),
    path('tasks/<int:pk>/delete/', views.TaskDeleteView.as_view(), name='task_delete'),

    # Category URLs (THIS FIXES YOUR ERROR)
    path('categories/', views.CategoryListView.as_view(), name='category_list'),
    path('categories/add/', views.CategoryCreateView.as_view(), name='category_add'),
    path('categories/<int:pk>/edit/', views.CategoryUpdateView.as_view(), name='category_edit'),
    path('categories/<int:pk>/delete/', views.CategoryDeleteView.as_view(), name='category_delete'),

    # Priority URLs
    path('priorities/', views.PriorityListView.as_view(), name='priority_list'),
    path('priorities/add/', views.PriorityCreateView.as_view(), name='priority_add'),
    path('priorities/<int:pk>/edit/', views.PriorityUpdateView.as_view(), name='priority_edit'),
    path('priorities/<int:pk>/delete/', views.PriorityDeleteView.as_view(), name='priority_delete'),

    # Note URLs
    path('notes/', views.NoteListView.as_view(), name='note_list'),
    path('notes/add/', views.NoteCreateView.as_view(), name='note_add'),
    path('notes/<int:pk>/edit/', views.NoteUpdateView.as_view(), name='note_edit'),
    path('notes/<int:pk>/delete/', views.NoteDeleteView.as_view(), name='note_delete'),

    # SubTask URLs
    path('subtasks/', views.SubTaskListView.as_view(), name='subtask_list'),
    path('subtasks/add/', views.SubTaskCreateView.as_view(), name='subtask_add'),
    path('subtasks/<int:pk>/edit/', views.SubTaskUpdateView.as_view(), name='subtask_edit'),
    path('subtasks/<int:pk>/delete/', views.SubTaskDeleteView.as_view(), name='subtask_delete'),

]
