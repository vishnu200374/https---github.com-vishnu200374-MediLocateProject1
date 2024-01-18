
from django.db import models
import os
# Create your models here.


class patientRegistration(models.Model):
    username = models.CharField(max_length=100, null=True)
    useremail = models.EmailField(null=True)
    password = models.CharField(max_length=100, null=True)
    address = models.CharField(max_length=100, null=True)
    profile = models.FileField(upload_to=os.path.join("static", "patients"))
    profilename = models.CharField(max_length=100, null=True)

    class Meta:
        db_table = "patientregistration"


class Patienthistory(models.Model):
    pid = models.CharField(max_length=100, null=True)
    itching = models.CharField(max_length=5, null=True)
    skin_rash = models.CharField(max_length=5, null=True)
    nodal_skin_eruptions = models.CharField(max_length=5, null=True)
    continuous_sneezing = models.CharField(max_length=5, null=True)
    shivering = models.CharField(max_length=5, null=True)
    chills = models.CharField(max_length=5, null=True)
    joint_pain = models.CharField(max_length=5, null=True)
    stomach_pain = models.CharField(max_length=5, null=True)
    acidity = models.CharField(max_length=5, null=True)
    ulcers_on_tongue = models.CharField(max_length=5, null=True)
    muscle_wasting = models.CharField(max_length=5, null=True)
    vomiting = models.CharField(max_length=5, null=True)
    burning_micturition = models.CharField(max_length=5, null=True)
    spotting_urination = models.CharField(max_length=5, null=True)
    fatigue = models.CharField(max_length=5, null=True)
    weight_gain = models.CharField(max_length=5, null=True)
    anxiety = models.CharField(max_length=5, null=True)
    cold_hands_and_feets = models.CharField(max_length=5, null=True)
    useremail = models.EmailField(null=True)
    disease = models.CharField(max_length=25, null=True)

    class Meta:
        db_table = "history"


class Requests(models.Model):
    slno = models.CharField(max_length=10, null=True)
    reqid = models.CharField(max_length=5, null=True)
    patientemail = models.EmailField(null=True)
    doctoremail = models.EmailField(null=True)
    appointmentdate = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, null=True)

    class Meta:
        db_table = "requests"


class BloodDonation(models.Model):
    blood_group = models.CharField(max_length=10, null=True)
    units = models.IntegerField(null=True)
    hospital_name = models.CharField(max_length=100, null=True)
    hospital_address = models.TextField(null=True)

    def __str__(self):
        return f"{self.blood_group} - {self.hospital_name}"

    class Meta:
        db_table = "BloodDonation"
