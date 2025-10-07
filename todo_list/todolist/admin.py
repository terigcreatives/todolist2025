from django.contrib import admin
from .models import Task

# Register your models here.

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "user", "parent_task", "priority", "due_date", "completed", "description", "created_at", "updated_at") #adjust fields as needed
    list_filter = ("completed", "priority", "user")
    search_fields = ("title", "description")