from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt
from django.conf.urls.static import static
from django.conf import settings


from . import views
app_name="trelloapp"
urlpatterns = [
    path('', auth_views.login, {'template_name':'trelloapp/home.html'}, name='index'),
    path('register/', views.register, name='register'),
    # path('login/', auth_views.login, {'template_name': 'trelloapp/login.html'}, name='login'),
    path('userlogin/', auth_views.login, {'template_name': 'trelloapp/userlogin.html'}, name='userlogin'),
    path('userhome/', views.userhome, name='userhome'),
    path('signup/', views.signup, name='signup'),
    path('logout/',views.logout_view,name='logout'),
    path('createproject/',views.createproject,name='createproject'),
    
    path('task/<int:id>/',views.createtask,name='createtask'),
    path('project/<int:id>/',csrf_exempt(views.projectpage),name='projectpage'),
    path('adduser/', csrf_exempt(views.adduser), name='adduser'),
    path('taskcompleted/',csrf_exempt(views.taskcompleted), name='taskcompleted')

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)