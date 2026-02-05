from django.contrib import admin
from .models import Priority, Category, Task, Note, SubTask
# Register your models here.

class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'deadline', 'category', 'priority')
    list_filter = ('status', 'category', 'priority')
    search_fields = ('title', 'description')
admin.site.register(Task, TaskAdmin)

class NoteAdmin(admin.ModelAdmin):
    list_display = ('task', 'content', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('content',)
admin.site.register(Note, NoteAdmin)

class SubTaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'parent_task')
    list_filter = ('status',)
    search_fields = ('title',)
admin.site.register(SubTask, SubTaskAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
admin.site.register(Category, CategoryAdmin)

class PriorityAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
admin.site.register(Priority, PriorityAdmin)
