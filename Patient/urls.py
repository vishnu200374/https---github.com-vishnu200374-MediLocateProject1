from django.urls import path, include
from . import views
urlpatterns = [
    path('patientsignup', views.patientsignup, name='patientsignup'),
    path('patientsignin', views.patientsignin, name="patientsignin"),
    path('symptoms', views.symptoms, name='symptoms'),
    path('doctorslist', views.doctorslist, name='doctorslist'),
    path('sendrequest/<int:id>', views.sendrequest, name='sendrequest'),
    path('myreports', views.myreports, name='myreports'),
    path('downloadfile/<int:reqid>/<str:filename>',
         views.downloadfile, name='downloadfile'),
    path('bloodgroup', views.bloodgroup, name="bloodgroup"),
    path('show_map/<str:hospital_address>', views.show_map, name="show_map"),

]
