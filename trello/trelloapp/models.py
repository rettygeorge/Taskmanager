from django.db import models
from django.contrib.auth.models import User


class Project(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=2000)
    projectmember= models.ManyToManyField(User, related_name='projectmember')
    def __str__(self):
    	return self.name

class Task(models.Model):
    PRIORITY_CHOICES = (
    	('low','Low'),
        ('medium','Medium'),
        ('high','High'),
  
    )
    project=models.ForeignKey(Project,on_delete=models.CASCADE)
    taskname = models.CharField(max_length=200)
    priority = models.CharField(max_length=200,choices=PRIORITY_CHOICES,default='High')
    taskdescription = models.TextField(max_length=2000)
    completed = models.BooleanField(default=False)
    
    def __str__(self):
    	return self.taskname



