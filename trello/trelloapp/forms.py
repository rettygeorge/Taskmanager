from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Project,Task


class BootstrapMixinForm(forms.ModelForm):
    """
    Sample Django Form To add Bootstrap's Form Control class to every field. 
    """
    def __init__(self, *args, **kwargs):
        super(BootstrapMixinForm, self).__init__(*args, **kwargs)
        for myField in self.fields:
            self.fields[myField].widget.attrs['class'] = 'form-control'


class RegistrationForm(BootstrapMixinForm, UserCreationForm):
    """
    User registration form

    The User table in models.py and UserCreation form is used
    """
	email=forms.EmailField(required=True)

	class Meta:
		model = User
		fields = ('username','email','password1','password2')

class ProjectCreationForm(forms.ModelForm):
    """
    Project creation form

    The table Project in models.py is used

    The name,description and picture fileds in Project table are used
    """

    class Meta:
        model = Project
        fields = ('name','description','picture')

class TaskCreationForm(forms.ModelForm):
    """
    Task creation form

    The table Task in models.py is used

    The taskname,priority and taskdescription in the Task table are used
    """

    class Meta:
        model = Task
        fields = ('taskname','priority','taskdescription')



