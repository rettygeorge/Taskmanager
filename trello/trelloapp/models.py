from django.db import models
from django.contrib.auth.models import User


class Project(models.Model):
    """
    Model for Project

    Attributes
    User : Foreignkey of User table
    name : char
         name of the project
    description : text
         Descrition of the project
    projectmember: manytomany field
         Members of the project
    picture : filefield
         Background image for the project
    """
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=2000)
    projectmember= models.ManyToManyField(User, related_name='projectmember')
    picture=models.FileField(blank=True)
    def __str__(self):
    	return self.name

class Task(models.Model):
    """
    Model for Task

    Attributes
    project : foreignkey of Project table
    taskname : char
            name of the task
    priority : char
            priority of the project, choices as low,high,medium
    taskdescription : text
            description of the task
    completed : boolean field
            marked as true if the task is completed
    completed_by :
            name of the user who completes the task
    """
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
    completed_by=models.CharField(max_length=200)
    
    def __str__(self):
    	return self.taskname



