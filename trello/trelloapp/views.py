from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, reverse
from .forms import RegistrationForm, ProjectCreationForm, TaskCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Project, Task, User
from django.db.models import Q
import json


def index(request):
	"""
	To display the homepage

	homepage contains the userlogin form
	"""
	return render(request,'trelloapp/home.html')


def register(request):
	"""
	User registration page
    
    The user data is collected using RegistrationForm()

    In POST method the user data is saved to the user table
	"""
	if request.method == 'POST':
		form = RegistrationForm(request.POST)
		# print(form)
		if form.is_valid():
			print('hiiiiiii')
			form.save()
			username=form.cleaned_data.get("username")
			raw_password = form.cleaned_data.get("password1")
			user=authenticate(username=username,password=raw_password)
			login(request,user)
			return redirect('trelloapp:index')
	else:
		form = RegistrationForm()
	
	return render(request, 'trelloapp/register.html', {'form':form})
@login_required(login_url='trelloapp:index')


def userhome(request):
	"""
	Userhome page

	The Project table and projectmember field is filtered based on the current user and the Queryset is passed to the template userhome.html

	This view is used to display the projects created by the current user and the projects in which the current users is added as a member
	"""
	print("required user",request.user)
	project_member=Project.objects.filter(projectmember__exact=request.user)
	obj_list=Project.objects.filter(user=request.user)
	return render(request,'trelloapp/userhome.html',{'obj':obj_list,'project_member':project_member})


def logout_view(request):
	"""
	Logout page

	"""
	logout(request)
	return render(request,'trelloapp/logout.html')


def createproject(request):
	"""
	Project creation page

	Project details are collected using ProjectCreationform and if the form is valid the data is saved to the Project table
	"""
	if request.method == 'POST':
		# form = ProjectCreationForm(request.POST, request.FILES)
		picture=request.FILES.get('picture')
		print(picture)
		name=request.POST.get('name')
		print(name)
		description = request.POST.get('description')
		print(description)
		
		project = Project(name=name, description=description,user=request.user,picture=picture)
		project.save()
		return redirect('trelloapp:userhome')
	else:
		form=ProjectCreationForm()
	return render(request,'trelloapp/createproject.html',{'form':form})


def projectpage(request,id):
	"""
	Detail page of each project

	Parameter : Project Id

	In the POST method the User table is filtered based on the values entered in the "search user" field in and the result is returned in the form of a list to the register2.html page"

	In the GET method the Project table is filtered based on the project id and the values in the corresponding projectmember field is passed to the template register2.html

	This detail page of a project can be accessed by the user who creates that project and the users who are members in that project otherwise redirected to an error page
	"""  

	if request.method == 'POST':
		
		name=request.POST.get('username')
		
	
		project=Project.objects.get(id=id)
		user_list = User.objects.filter(Q(username__contains=name)).exclude(id=request.user.id).exclude(id__in=[x.id for x in Project.objects.filter(id=id).first().projectmember.all().only('id')]).values_list('username', flat=True)
		users=list(user_list)
		
		return HttpResponse(json.dumps({"usernames":users,"projectid":id}),content_type="application/json")
	else:
		project=Project.objects.get(id=id)
		projectmember=project.projectmember.all()
		print("project members",projectmember)
		project_member=project.projectmember.all().values_list('username',flat=True)
		print("project member list",list(project_member))
		print("project created",project.user)
		print("current user",request.user)
		

		task_list=Task.objects.filter(project=project).order_by("-completed")
		
		if(request.user==project.user or (request.user.username in list(project_member))):
			print("hai")	
			return render(request,'trelloapp/register2.html',{'project':project,'task_list':task_list,'projectmember':projectmember})
		else:
			print("hello")
			return render(request,'trelloapp/notamember.html')
		return HttpResponse()


def createtask(request,id):

	"""
	Task creation page

	The task details is collected from the project using the TaskCreationForm

	In the POST method the task details is save to the table Task

	The task creation page of a project can be accessed by the user who creates that project and the users who are members in that project otherwise redirected to an error page
	"""
	
	project=Project.objects.get(id=id)
	if request.method == 'POST':
		taskname=request.POST.get('taskname')
		priority = request.POST.get('priority')
		taskdescription = request.POST.get('taskdescription')
		
		task = Task(taskname=taskname, priority=priority,taskdescription=taskdescription,project=project)
		task.save()
		url = reverse(('trelloapp:projectpage'), kwargs={ 'id': id })
		return HttpResponseRedirect(url)
		
	else:
		form=TaskCreationForm()
		project=Project.objects.get(id=id)
		project_member=project.projectmember.all().values_list('username',flat=True)
		if(request.user==project.user or request.user.username in list(project_member)):
			return render(request,'trelloapp/task.html',{'form':form})
		else:
			return render(request,'trelloapp/notamember.html')


def adduser(request,*args, **kwargs):
	"""
	To add users to a project

	The users are added to the manytomany field projectmember in the table Project

	"""
	print(id)
	if request.method == 'POST':
		username=request.POST.get('username')
		projectid=request.POST.get('projectid')
		print(projectid)

		project = Project.objects.filter(id=request.POST.get('projectid')).first()
		user = User.objects.filter(username=request.POST.get('username')).first()

		if user and project:
			project.projectmember.add(user)
			project=Project.objects.get(id=projectid)
			projectmember=project.projectmember.all().values_list('username',flat=True)
			print(projectmember)
			
			return HttpResponse(json.dumps({"usernames":list(projectmember)}),content_type="application/json")
		return HttpResponse('failed')		
	return HttpResponse('Get Request Not Allowed')	


def taskcompleted(request):
	"""
	To mark the task as completed
	"""
	if request.method == 'POST':
		taskid=request.POST.get('taskid')
		
		print(request.user)
		task=Task.objects.get(id=taskid)
		task.completed=True
		task.completed_by=request.user.username
		task.save()
		task=Task.objects.get(id=taskid)
		print(task.completed_by)
		return JsonResponse({'taskcompleted':task.completed_by,'taskid':taskid})


def signup(request):
	"""
	User registration page
    
    The user data is collected using RegistrationForm()

    In POST method the user data is saved to the user table
	"""
	if request.method == 'POST':
		form = RegistrationForm(request.POST)
	
		if form.is_valid():
			print('hiiiiiii')
			form.save()
			username=form.cleaned_data.get("username")
			raw_password = form.cleaned_data.get("password1")
			user=authenticate(username=username,password=raw_password)
			login(request,user)
			return redirect('trelloapp:index')
	else:
		form = RegistrationForm()
	
	return render(request, 'trelloapp/signup.html', {'form':form})