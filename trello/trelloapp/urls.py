from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf.urls import url

from . import views
app_name="trelloapp"
urlpatterns = [
    path('', auth_views.login, {'template_name':'trelloapp/home.html'}, name='index'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.login, {'template_name': 'trelloapp/login.html'}, name='login'),
    path('userhome/', views.userhome, name='userhome'),
    path('logout/',views.logout_view,name='logout'),
    path('createproject/',views.createproject,name='createproject'),
    
    path('task/<int:id>/',views.createtask,name='createtask'),
    path('project/<int:id>/',views.projectpage,name='projectpage'),

]