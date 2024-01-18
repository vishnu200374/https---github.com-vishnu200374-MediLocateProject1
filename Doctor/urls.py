from django.urls import path,include
from . import views
urlpatterns = [
    path('',views.index,name='index'),
    path('docsignup',views.docsignup,name='docsignup'),
    path('docsignin',views.docsignin,name='docsignin'),
    path('viewappointments',views.viewappointments,name='viewappointments'),
    path('reportview/<int:id>/<int:reqid>',views.reportview,name='reportview'),
    path('uploadreport/<int:pid>',views.uploadreport,name='uploadreport'),
    path('fileupload',views.fileupload,name='fileupload'),
    path('viewreports',views.viewreports,name='viewreports'),
    path('sendkey/<int:reqid>',views.sendkey,name='sendkey'),
]
