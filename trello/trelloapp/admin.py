from django.contrib import admin
from .models import Project, Task
# Register your models here.
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'description','picture')
admin.site.register(Project,ProjectAdmin)

# Register your models here.
class TaskAdmin(admin.ModelAdmin):
    list_display = ('project', 'taskname', 'priority','taskdescription','completed','completed_by')
admin.site.register(Task,TaskAdmin)

