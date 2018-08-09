from django.db import models
from django.contrib.auth.models import User


class Project(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=2000)
    def __str__(self):
    	return self.name

class Task(models.Model):
    project=models.ForeignKey(Project,on_delete=models.CASCADE)
    taskname = models.CharField(max_length=200)
    priority = models.CharField(max_length=200)
    taskdescription = models.TextField(max_length=2000)
    def __str__(self):
    	return self.taskname


