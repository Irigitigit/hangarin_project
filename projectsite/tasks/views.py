from multiprocessing import context
from urllib import request
from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Task, Priority, Category, Note, SubTask
from django.utils import timezone
from datetime import timedelta
from django import forms
from django.db.models import Q

def home_view(request):
    now = timezone.now()
    three_days_from_now = now + timedelta(days=3)

    # 1. High Priority Tasks
    # Assumes your Priority model has a name field like 'High'
    # TEMPORARY TEST: Change the filter to this to see if ANY tasks show up
    active_critical_tasks = Task.objects.filter(
        (Q(priority__name__icontains='High') | Q(priority__name__icontains='Crit'))
    ).exclude(status__iexact='Completed').select_related('priority', 'category').order_by('-id')

    # 2. Tasks Due Soon (Next 3 days)   
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
class TaskListView(ListView):
    model = Task
    context_object_name = 'items'
    template_name = 'task_list.html'

    def get_queryset(self):
        # 1. Start with the base queryset
        queryset = Task.objects.all().select_related('priority', 'category')
        
        # 2. Grab filters from the request
        query = self.request.GET.get('q')
        priority_filter = self.request.GET.get('priority')
        category_filter = self.request.GET.get('category')
        status_filter = self.request.GET.get('status')

        # 3. Apply filters if they exist
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) | Q(description__icontains=query)
            )
        
        if category_filter:
            queryset = queryset.filter(category__name__iexact=category_filter)
        if priority_filter:
            queryset = queryset.filter(priority__name__iexact=priority_filter)
            
        if status_filter:
            queryset = queryset.filter(status__iexact=status_filter)

        # 4. Return the QuerySet (Django handles the rendering automatically)
        return queryset.order_by('-id')

    def get_context_data(self, **kwargs):
        # This keeps your search/filter values "sticky" in the search bars/dropdowns
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        context['selected_priority'] = self.request.GET.get('priority', '')
        context['selected_status'] = self.request.GET.get('status', '')
        return context


class TaskCreateView(CreateView):
    model = Task
    fields = ['title', 'description', 'deadline', 'status', 'category', 'priority']
    template_name = 'common_form.html'
    success_url = reverse_lazy('task_list')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # We change the 'deadline' widget to use the HTML5 datetime-local picker
        form.fields['deadline'].widget = forms.DateTimeInput(
            attrs={'type': 'datetime-local', 'class': 'form-control'},
            format='%Y-%m-%dT%H:%M'
        )
        return form

    def form_invalid(self, form):
        print("Form Errors:", form.errors) # This helps you debug in the terminal
        return super().form_invalid(form)

class TaskUpdateView(UpdateView):
    model = Task
    fields = ['title', 'description', 'deadline', 'status', 'category', 'priority']
    template_name = 'common_form.html'
    success_url = reverse_lazy('task_list')

class TaskDeleteView(DeleteView):
    model = Task
    template_name = 'common_confirm_delete.html'
    success_url = reverse_lazy('task_list')



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
    template_name = 'priority_list.html'
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
    fields = ['title', 'status', 'parent_task']
    template_name = 'common_form.html'
    success_url = reverse_lazy('home')

class SubTaskUpdateView(UpdateView):
    model = SubTask
    fields = ['title', 'status', 'parent_task']
    template_name = 'common_form.html'
    success_url = reverse_lazy('home')

class SubTaskDeleteView(DeleteView):
    model = SubTask
    template_name = 'common_confirm_delete.html'
    success_url = reverse_lazy('home')

# (Repeat similar classes for Note and SubTask as needed)
