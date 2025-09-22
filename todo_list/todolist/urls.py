from django.urls import path
from . import views

#url configuration
urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('contact/', views.contact, name='contact_us'),
    path('alltasks/', views.tasklist, name='task_list'),
    path('today/', views.tasklist, name='today'),
    path('tomorrow/', views.tasklist, name='tomorrow'),
    path('week/', views.tasklist, name='this_week'),
    path('planned/', views.tasklist, name='planned'),
    path('completed/', views.tasklist, name='completed'),
    path('editTask/<int:id>', views.edit_task, name='edit_task'),
    path('task/delete/<int:pk>/', views.delete_task, name='delete_task'),
    path('task/add_task/', views.add_task, name='add_task'),
    path('subtask/toggle/<int:subtask_id>/', views.toggle_subtask, name='toggle_subtask'),
    
]