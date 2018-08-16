from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, reverse
from .forms import RegistrationForm, ProjectCreationForm, TaskCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Project, Task, User
from django.db.models import Q
import json


def index(request):
    return render(request,'trelloapp/home.html')
def register(request):
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
	
	obj_list=Project.objects.filter(user=request.user)
	return render(request,'trelloapp/userhome.html',{'obj':obj_list})

def logout_view(request):
	logout(request)
	return render(request,'trelloapp/logout.html')
def createproject(request):
	if request.method == 'POST':
		name=request.POST.get('name')
		description = request.POST.get('description')
		# body = request.POST.get('body')
		# response_data = {}
		project = Project(name=name, description=description,user=request.user)
		project.save()
		return redirect('trelloapp:userhome')
	else:
		form=ProjectCreationForm()
	return render(request,'trelloapp/createproject.html',{'form':form})
def projectpage(request,id):
	

	# print(project)
	# print(request.POST)
	if request.method == 'POST':
		# import pdb;
		# pdb.set_trace()
		name=request.POST.get('username')
		# print(name)
	
		project=Project.objects.get(id=id)
		user_list = User.objects.filter(Q(username__contains=name)).exclude(id=request.user.id).exclude(id__in=[x.id for x in Project.objects.filter(id=id).first().projectmember.all().only('id')]).values_list('username', flat=True)
		users=list(user_list)
		# projectmember=project.projectmember.all().values_list('username',flat=True)
		# print(projectmember)
		# # users.remove(project.user)
		# for user in list(user_list):
		# 	for user1 in list(projectmember):
		# 		if(user1==user):
		# 			users.remove(user)
		# print(users)
		return HttpResponse(json.dumps({"usernames":users,"projectid":id}),content_type="application/json")
	else:
		project=Project.objects.get(id=id)
		projectmember=project.projectmember.all()
		print(projectmember)
		project_member=project.projectmember.all().values_list('username',flat=True)
		print(list(project_member))
		print(project.user)
		print(request.user)
		

		task_list=Task.objects.filter(project=project).order_by("-completed")
		if(request.user==project.user or request.user in list(project_member)):
				
			return render(request,'trelloapp/register2.html',{'project':project,'task_list':task_list,'projectmember':projectmember})
		else:
			return render(request,'trelloapp/notamember.html')
		return HttpResponse()

def createtask(request,id):
	# print(type(projectid))
	project=Project.objects.get(id=id)
	if request.method == 'POST':
		taskname=request.POST.get('taskname')
		priority = request.POST.get('priority')
		taskdescription = request.POST.get('taskdescription')
		# response_data = {}
		task = Task(taskname=taskname, priority=priority,taskdescription=taskdescription,project=project)
		task.save()
		url = reverse(('trelloapp:projectpage'), kwargs={ 'id': id })
		return HttpResponseRedirect(url)
		# return redirect('trelloapp:projectpage','id'=id)
	else:
		form=TaskCreationForm()
		project=Project.objects.get(id=id)
		project_member=project.projectmember.all().values_list('username',flat=True)
		if(request.user==project.user or request.user in list(project_member)):
			return render(request,'trelloapp/task.html',{'form':form})
		else:
			return render(request,'trelloapp/notamember.html')

def adduser(request,*args, **kwargs):
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
	if request.method == 'POST':
		taskid=request.POST.get('taskid')
		task=Task.objects.get(id=taskid)
		task.completed=True
		task.save()
		return HttpResponse()
def signup(request):
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
	
	return render(request, 'trelloapp/signup.html', {'form':form})