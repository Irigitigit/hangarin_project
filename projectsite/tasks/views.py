from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Task, Priority, Category, Note, SubTask

# --- TASK CRUD ---
class TaskListView(ListView):
    model = Task
    context_object_name = 'tasks'
    template_name = 'home.html'

class TaskCreateView(CreateView):
    model = Task
    fields = '__all__'
    template_name = 'common_form.html'
    success_url = reverse_lazy('home')

class TaskUpdateView(UpdateView):
    model = Task
    fields = '__all__'
    template_name = 'common_form.html'
    success_url = reverse_lazy('home')

class TaskDeleteView(DeleteView):
    model = Task
    template_name = 'common_confirm_delete.html'
    success_url = reverse_lazy('home')



# --- CATEGORY ---
class CategoryListView(ListView):
    model = Category
    template_name = 'category_list.html'
    context_object_name = 'items'

class CategoryCreateView(CreateView):
    model = Category
    fields = ['name']
    template_name = 'common_form.html'
    success_url = reverse_lazy('category_list')

class CategoryUpdateView(UpdateView):
    model = Category
    fields = ['name']
    template_name = 'common_form.html'
    success_url = reverse_lazy('category_list')

class CategoryDeleteView(DeleteView):
    model = Category
    template_name = 'common_confirm_delete.html'
    success_url = reverse_lazy('category_list')

# --- PRIORITY ---
class PriorityListView(ListView):
    model = Priority
    template_name = 'priority_list.html' # You can create this next
    context_object_name = 'items'

class PriorityCreateView(CreateView):
    model = Priority
    fields = ['name']
    template_name = 'common_form.html'
    success_url = reverse_lazy('priority_list')

class PriorityUpdateView(UpdateView):
    model = Priority
    fields = ['name']
    template_name = 'common_form.html'
    success_url = reverse_lazy('priority_list')

class PriorityDeleteView(DeleteView):
    model = Priority
    template_name = 'common_confirm_delete.html'
    success_url = reverse_lazy('priority_list')

class NoteListView(ListView):
    model = Note
    template_name = 'note_list.html'
    context_object_name = 'items'

class NoteCreateView(CreateView):
    model = Note
    fields = ['content', 'task']
    template_name = 'common_form.html'
    success_url = reverse_lazy('home')

class NoteUpdateView(UpdateView):
    model = Note
    fields = ['content', 'task']
    template_name = 'common_form.html'
    success_url = reverse_lazy('home')

class NoteDeleteView(DeleteView):
    model = Note
    template_name = 'common_confirm_delete.html'
    success_url = reverse_lazy('home')

class SubTaskListView(ListView):    
    model = SubTask
    template_name = 'subtask_list.html'
    context_object_name = 'items'

class SubTaskCreateView(CreateView):
    model = SubTask
    fields = ['name', 'task']
    template_name = 'common_form.html'
    success_url = reverse_lazy('home')

class SubTaskUpdateView(UpdateView):
    model = SubTask
    fields = ['name', 'task']
    template_name = 'common_form.html'
    success_url = reverse_lazy('home')

class SubTaskDeleteView(DeleteView):
    model = SubTask
    template_name = 'common_confirm_delete.html'
    success_url = reverse_lazy('home')

# (Repeat similar classes for Note and SubTask as needed)
