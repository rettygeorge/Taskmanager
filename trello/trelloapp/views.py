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
@login_required(login_url='trelloapp:login')
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
		user_list=User.objects.filter(Q(username__contains=name)).values_list('username',flat=True)
		# print(user_list)
		return HttpResponse(json.dumps({"usernames":list(user_list),"projectid":id}),content_type="application/json")
	else:
		project=Project.objects.get(id=id)
		task_list=Task.objects.filter(project=project).order_by("-completed")
		return render(request,'trelloapp/register2.html',{'project':project,'task_list':task_list})


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
	return render(request,'trelloapp/task.html',{'form':form})

def adduser(request,self, *args, **kwargs):
	if request.method == 'POST':
		projectid=request.POST.get('projectid')
		print(projectid)
		username=request.POST.get('username')
		print(username)
		user=User.objects.get(username=username)
		# print("projectname",project)
		self.projectmember.add(user)

def taskcompleted(request):
	if request.method == 'POST':
		taskid=request.POST.get('taskid')
		task=Task.objects.get(id=taskid)
		task.completed=True
		task.save()
		return HttpResponse()
