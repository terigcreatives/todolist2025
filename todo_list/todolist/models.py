from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) # link to user
    priority_choices = [
        ('L', 'Low'),
        ('M', 'Medium'),
        ('H', 'High'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    priority = models.CharField(
        max_length=1,
        choices=priority_choices,
        default='M',
    )
    due_date = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Self-referencing field for subtasks 
    parent_task = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='subtasks',
        blank=True,
        null=True,
    )

    def __str__(self):
        if self.parent_task:
            return f"{self.title} (Subtask of {self.parent_task.title})"
        return f"{self.title} ({self.get_priority_display()})"
    
    @property
    def completed_subtasks_count(self):
        # Count all completed subtasks including grandchildren (recursively).
        completed = self.subtasks.filter(completed=True).count()
        for sub in self.subtasks.all():
            completed += sub.completed_subtasks_count
        return completed
    
    @property
    def total_subtasks_count(self):
        # Count all subtasks including grandchildren (recursively).
        total = self.subtasks.count()
        for sub in self.subtasks.all():
            total += sub.total_subtasks_count
        return total
