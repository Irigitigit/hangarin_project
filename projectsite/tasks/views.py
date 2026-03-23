from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Task, Priority, Category, Note, SubTask
from django.utils import timezone
from datetime import timedelta
from django import forms
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

# --- DASHBOARD & ABOUT ---
@login_required
def home_view(request):
    now = timezone.now()
    three_days_from_now = now + timedelta(days=3)

    active_critical_tasks = Task.objects.filter(
        (Q(priority__name__icontains='High') | Q(priority__name__icontains='Crit'))
    ).exclude(status__iexact='Completed').select_related('priority', 'category').order_by('-id')

    urgent_tasks = Task.objects.filter(
        deadline__range=[now, three_days_from_now]
    ).order_by('deadline')

    context = {
        'total_tasks': Task.objects.count(),
        'total_categories': Category.objects.count(),
        'total_notes': Note.objects.count(),
        'my_tasks': active_critical_tasks,
        'urgent_tasks': urgent_tasks,
    }
    return render(request, 'home.html', context)

def about_view(request):
    return render(request, 'about.html')


# --- TASK CRUD ---
class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'items'
    template_name = 'task_list.html'

    def get_queryset(self):
        queryset = Task.objects.all().select_related('priority', 'category')
        query = self.request.GET.get('q')
        priority_filter = self.request.GET.get('priority')
        category_filter = self.request.GET.get('category')
        status_filter = self.request.GET.get('status')

        if query:
            queryset = queryset.filter(Q(title__icontains=query) | Q(description__icontains=query))
        if category_filter:
            queryset = queryset.filter(category__name__iexact=category_filter)
        if priority_filter:
            queryset = queryset.filter(priority__name__iexact=priority_filter)
        if status_filter:
            queryset = queryset.filter(status__iexact=status_filter)

        return queryset.order_by('-id')

class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'description', 'deadline', 'status', 'category', 'priority']
    template_name = 'common_form.html'
    success_url = reverse_lazy('task_list')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['deadline'].widget = forms.DateTimeInput(
            attrs={'type': 'datetime-local', 'class': 'form-control'},
            format='%Y-%m-%dT%H:%M'
        )
        return form

class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title', 'description', 'deadline', 'status', 'category', 'priority']
    template_name = 'common_form.html'
    success_url = reverse_lazy('task_list')

class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'common_confirm_delete.html'
    success_url = reverse_lazy('task_list')


# --- CATEGORY CRUD ---
class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'category_list.html'
    context_object_name = 'items'

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(name__icontains=query)
        return queryset.order_by('name')

class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    fields = ['name']
    template_name = 'common_form.html'
    success_url = reverse_lazy('category_list')

class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = Category
    fields = ['name']
    template_name = 'common_form.html'
    success_url = reverse_lazy('category_list')

class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = Category
    template_name = 'common_confirm_delete.html'
    success_url = reverse_lazy('category_list')


# --- PRIORITY CRUD ---
class PriorityListView(LoginRequiredMixin, ListView):
    model = Priority
    template_name = 'priority_list.html'
    context_object_name = 'items'

class PriorityCreateView(LoginRequiredMixin, CreateView):
    model = Priority
    fields = ['name']
    template_name = 'common_form.html'
    success_url = reverse_lazy('priority_list')

class PriorityUpdateView(LoginRequiredMixin, UpdateView):
    model = Priority
    fields = ['name']
    template_name = 'common_form.html'
    success_url = reverse_lazy('priority_list')

class PriorityDeleteView(LoginRequiredMixin, DeleteView):
    model = Priority
    template_name = 'common_confirm_delete.html'
    success_url = reverse_lazy('priority_list')


# --- NOTE CRUD ---
class NoteListView(LoginRequiredMixin,ListView):
    model = Note
    template_name = 'note_list.html'
    context_object_name = 'items'

    def get_queryset(self):
        queryset = super().get_queryset().select_related('task')
        query = self.request.GET.get('q')
        date_filter = self.request.GET.get('date')

        if query:
            queryset = queryset.filter(content__icontains=query)
        if date_filter:
            queryset = queryset.filter(created_at__date=date_filter)

        return queryset.order_by('-created_at')

class NoteCreateView(LoginRequiredMixin, CreateView):
    model = Note
    fields = ['content', 'task']
    template_name = 'common_form.html'
    success_url = reverse_lazy('note_list') 

class NoteUpdateView(LoginRequiredMixin, UpdateView):
    model = Note
    fields = ['content', 'task']
    template_name = 'common_form.html'
    success_url = reverse_lazy('note_list')

class NoteDeleteView(LoginRequiredMixin, DeleteView):
    model = Note
    template_name = 'common_confirm_delete.html'
    success_url = reverse_lazy('note_list')


# --- SUBTASK CRUD ---
class SubTaskListView(LoginRequiredMixin, ListView):    
    model = SubTask
    template_name = 'subtask_list.html'
    context_object_name = 'items'

    def get_queryset(self):
        # Added select_related for better performance
        queryset = super().get_queryset().select_related('parent_task')
        query = self.request.GET.get('q')
        status_filter = self.request.GET.get('status')
        
        if query:
            queryset = queryset.filter(title__icontains=query)
        if status_filter:
            queryset = queryset.filter(status=status_filter)

        return queryset

class SubTaskCreateView(LoginRequiredMixin, CreateView):
    model = SubTask
    fields = ['title', 'status', 'parent_task']
    template_name = 'common_form.html'
    success_url = reverse_lazy('subtask_list')

class SubTaskUpdateView(LoginRequiredMixin, UpdateView):
    model = SubTask
    fields = ['title', 'status', 'parent_task']
    template_name = 'common_form.html'
    success_url = reverse_lazy('subtask_list')

class SubTaskDeleteView(LoginRequiredMixin, DeleteView):
    model = SubTask
    template_name = 'common_confirm_delete.html'
    success_url = reverse_lazy('subtask_list')