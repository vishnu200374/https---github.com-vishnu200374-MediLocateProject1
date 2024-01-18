from django.db import models
import os

# Create your models here.


class DocRegistration(models.Model):
    username = models.CharField(max_length=100, null=True)
    useremail = models.EmailField(null=True)
    password = models.CharField(max_length=100, null=True)
    department = models.CharField(max_length=100, null=True)
    address = models.CharField(max_length=100, null=True)
    profile = models.FileField(upload_to=os.path.join("static", "profiles"))
    profilename = models.CharField(max_length=100, null=True)
    hospitalname = models.CharField(max_length=100, null=True)
    hospitaladdress = models.TextField(null=True)

    class Meta:
        db_table = "doctorregistration"


class Reportupload(models.Model):
    reqid = models.CharField(max_length=20, null=True)
    filename = models.CharField(max_length=20, null=True)
    myfile = models.FileField(upload_to=os.path.join('static', 'reports'))
    patientemail = models.EmailField(null=True)
    doctoremail = models.EmailField(null=True)
    filecontent = models.TextField(null=True)
    key = models.TextField(null=True)

    class Meta:
        db_table = 'reports'
