from django.core.management.base import BaseCommand
from faker import Faker
from django.utils import timezone

from tasks.models import Priority, Category, Task, Note, SubTask

class Command(BaseCommand):
    help = 'Create initial data for tasks app'

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Create Priorities
        priorities = ['Low', 'Medium', 'High', 'Critical', 'Optional']
        for priority_name in priorities:
            Priority.objects.get_or_create(name=priority_name)
        self.stdout.write(self.style.SUCCESS('Successfully created priorities.'))

        # Create Categories
        categories = ['Work', 'School', 'Personal', 'Personal', "Projects"]
        for category_name in categories:
            Category.objects.get_or_create(name=category_name)
        self.stdout.write(self.style.SUCCESS('Successfully created categories.'))

        # Create Tasks
        for _ in range(10):
            category = Category.objects.order_by('?').first()
            priority = Priority.objects.order_by('?').first()

            deadline_date=timezone.make_aware(fake.date_time_this_month())

            task = Task.objects.create(
                title=fake.sentence(nb_words=5),
                description=fake.paragraph(nb_sentences=3),
                deadline=deadline_date,
                status=fake.random_element(elements=["Pending", "In Progress", "Completed"]),
                category=category,
                priority=priority
            )

            # Create Notes for each Task
            for _ in range(2):
                Note.objects.create(
                    task=task,
                    content=fake.paragraph(nb_sentences=2)
                )

            # Create SubTasks for each Task
            for _ in range(3):
                SubTask.objects.create(
                    parent_task=task,
                    title=fake.sentence(nb_words=4),
                    status=fake.random_element(elements=["Pending", "In Progress", "Completed"])
                )

        self.stdout.write(self.style.SUCCESS('Successfully created tasks, notes, and subtasks.'))