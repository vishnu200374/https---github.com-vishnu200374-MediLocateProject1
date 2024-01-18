from django.shortcuts import render, redirect
from . models import patientRegistration, Patienthistory, Requests, BloodDonation
from Doctor.models import DocRegistration, Reportupload
from django.contrib import messages
import pickle
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404
from Crypto.Cipher import AES
import requests
import folium
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from django.conf import settings
import googlemaps
key = get_random_bytes(32)
block_size = 16


# template
PATIENTSIGNUPPAGE = "patientsignup.html"
PATIENTSIGNINPAGE = "patientsignin.html"
PATIENTHOMEPAGE = "patienthome.html"
SYMPTOMSPAGE = "symptoms.html"
DOCTORSLISTPAGE = "doctorslist.html"
MYREPORTSPAGE = "myreports.html"
MYFILEPAGE = "mine.html"
BLOOD_GROUP = "bloodgroup.html"

# Create your views here.


def generatebloodgroup():
    blood_groups = ['A+', 'A-', 'B+', 'B-', 'O+', 'O-', 'AB+', 'AB-']
    for i in blood_groups:
        data = [(i.hospitalname, i.hospitaladdress)
                for i in DocRegistration.objects.all().order_by('?')][0]

        blood_check = BloodDonation.objects.filter(
            hospital_name=data[0], hospital_address=data[1]).exists()
        if blood_check:
            print("Details already exists")
        else:
            donation = BloodDonation.objects.create(
                blood_group=i, units=10, hospital_name=data[0], hospital_address=data[1])
            donation.save()
    return "Success"


def patientsignup(req):
    if req.method == "POST":
        username = req.POST['username']
        useremail = req.POST['useremail']
        password = req.POST['password']
        confirmpassword = req.POST['confirmpassword']
        address = req.POST['address']
        profile = req.FILES['profile']
        profilename = profile.name
        if password == confirmpassword:
            data = patientRegistration.objects.filter(
                useremail=useremail, password=password).exists()
            if data:
                messages.info(req, "Account already exist with these details")
                return redirect("patientsignin")
            dc = patientRegistration(username=username, useremail=useremail, password=password,
                                     address=address.lower(), profile=profile, profilename=profilename)
            dc.save()
            messages.info(req, "Patient Registration success")
            return redirect("patientsignin")
        messages.error(req, "Password & confirm passwords are not matching")
        return render(req, PATIENTSIGNUPPAGE)
    return render(req, PATIENTSIGNUPPAGE)


def patientsignin(req):
    if req.method == "POST":
        useremail = req.POST['useremail']
        password = req.POST['password']
        dc = patientRegistration.objects.filter(
            useremail=useremail, password=password).exists()
        if dc:
            pro = patientRegistration.objects.filter(
                useremail=useremail, password=password)
            profilename = [i.profilename for i in pro][0]
            req.session['useremail'] = useremail
            req.session['patientprofile'] = profilename
            return render(req, PATIENTHOMEPAGE, {'profile': profilename})
        messages.error(req, "Invalid Credentials")
        return render(req, PATIENTSIGNINPAGE)
    return render(req, PATIENTSIGNINPAGE)


def symptoms(req):
    pid = [i.id for i in patientRegistration.objects.filter(
        useremail=req.session['useremail'])]
    print(pid)
    if req.method == "POST":
        itching = str(req.POST['itching'])
        skin_rash = str(req.POST['skin_rash'])
        nodal_skin_eruptions = str(req.POST['nodal_skin_eruptions'])
        continuous_sneezing = str(req.POST['continuous_sneezing'])
        shivering = str(req.POST['shivering'])
        chills = str(req.POST['chills'])
        joint_pain = str(req.POST['joint_pain'])
        stomach_pain = str(req.POST['stomach_pain'])
        acidity = str(req.POST['acidity'])
        ulcers_on_tongue = str(req.POST['ulcers_on_tongue'])
        muscle_wasting = str(req.POST['muscle_wasting'])
        vomiting = str(req.POST['vomiting'])
        burning_micturition = str(req.POST['burning_micturition'])
        spotting_urination = str(req.POST['spotting_urination'])
        fatigue = str(req.POST['fatigue'])
        weight_gain = str(req.POST['weight_gain'])
        anxiety = str(req.POST['anxiety'])
        cold_hands_and_feets = str(req.POST['cold_hands_and_feets'])
        newdata = [[itching, skin_rash, nodal_skin_eruptions, continuous_sneezing, shivering,
                    chills, joint_pain, stomach_pain, acidity, ulcers_on_tongue, muscle_wasting,
                    vomiting, burning_micturition, spotting_urination, fatigue, weight_gain,
                    anxiety, cold_hands_and_feets]]
        df = pd.read_csv('static/dataset/Training.csv')
        df.head()
        df.isnull().sum()
        df = df[['itching', 'skin_rash', 'nodal_skin_eruptions', 'continuous_sneezing', 'shivering',
                 'chills', 'joint_pain', 'stomach_pain', 'acidity', 'ulcers_on_tongue', 'muscle_wasting',
                 'vomiting', 'burning_micturition', 'spotting_ urination', 'fatigue', 'weight_gain',
                 'anxiety', 'cold_hands_and_feets', 'prognosis']]
        x = df.drop(['prognosis'], axis=1)
        y = df['prognosis']
        x_train, x_test, y_train, y_test = train_test_split(
            x, y, test_size=0.3, random_state=42)
        rf = RandomForestClassifier()
        rf.fit(x_train, y_train)
        result = rf.predict(newdata)
        result = result[0]
        msg = f'The predicted disease is {result}'
        dc = Patienthistory(
            itching=itching,
            skin_rash=skin_rash,
            nodal_skin_eruptions=nodal_skin_eruptions,
            continuous_sneezing=continuous_sneezing,
            shivering=shivering,
            chills=chills,
            joint_pain=joint_pain,
            stomach_pain=stomach_pain,
            acidity=acidity,
            ulcers_on_tongue=ulcers_on_tongue,
            muscle_wasting=muscle_wasting,
            vomiting=vomiting,
            burning_micturition=burning_micturition,
            spotting_urination=spotting_urination,
            fatigue=fatigue,
            weight_gain=weight_gain,
            anxiety=anxiety,
            cold_hands_and_feets=cold_hands_and_feets,
            useremail=req.session['useremail'],
            disease=result, pid=pid[0])
        dc.save()
        return render(req, SYMPTOMSPAGE, {'profile': req.session['patientprofile'], 'msg': msg, 'useremail': req.session['useremail']})
    return render(req, SYMPTOMSPAGE, {'profile': req.session['patientprofile']})


def doctorslist(req):
    useremail = req.session['useremail']

    data = [(i.id, i.address)
            for i in patientRegistration.objects.filter(useremail=useremail)]
    print(data)
    id = data[0][0]
    req.session['userid'] = id
    address = data[0][1]
    dc = [i for i in DocRegistration.objects.filter(address=address)]
    print(dc)
    print("=======")
    return render(req, DOCTORSLISTPAGE, {'dc': dc, 'id': id, 'profile': req.session['patientprofile']})


def sendrequest(req, id):
    dc = [(i.id, i.useremail) for i in DocRegistration.objects.filter(id=id)]
    patientemail = req.session['useremail']
    dc = Requests(slno=id, reqid=req.session['userid'],
                  patientemail=patientemail, doctoremail=dc[0][1], status='pending')
    dc.save()
    messages.success(req, 'Appointment Request sent successfully')
    return redirect("doctorslist")


def myreports(req):
    dc = Reportupload.objects.filter(patientemail=req.session['useremail'])
    return render(req, MYREPORTSPAGE, {'profile': req.session['patientprofile'], 'dc': dc})


def downloadfile(req, reqid, filename):
    dc = [(i.filename, i.key, i.filecontent)
          for i in Reportupload.objects.filter(reqid=reqid, filename=filename)]
    print(dc)
    filename = dc[0][0]
    content = dc[0][2]
    file_path = "static/reports/{}".format(dc[0][0])
    print(filename, content)
    with open(file_path, 'r') as file:
        content = file.read()
    return render(req, MYFILEPAGE, {'profile': req.session['patientprofile'], 'content': content, 'filename': filename})


def bloodgroup(req):
    data = BloodDonation.objects.all()
    if req.method == "POST":
        blood_group = req.POST['search']
        bloodgroup_data = BloodDonation.objects.filter(blood_group=blood_group)
        print(bloodgroup_data)
        return render(req, BLOOD_GROUP, {'profile': req.session['patientprofile'], 'data': generatebloodgroup(), 'data': bloodgroup_data})
    return render(req, BLOOD_GROUP, {'profile': req.session['patientprofile'], 'data': generatebloodgroup(), 'data': data})


def show_map(req, hospital_address):
    address = hospital_address
    gmaps = googlemaps.Client(key=settings.GOOGLE_MAPS_API_KEY)
    geocode_result = gmaps.geocode(address)

    if not geocode_result:
        # Handle the case when the address is not valid
        return render(req, 'error.html', {'error_message': 'Invalid address'})

    # Extract latitude and longitude from the geocode result
    location = geocode_result[0]['geometry']['location']
    lat, lng = location['lat'], location['lng']
    print(address)
    print(lat, lng)
    mymap = folium.Map(location=[lat, lng], zoom_start=12)

    # Add a marker at a specific location
    folium.Marker(location=[lat, lng], popup='San Francisco').add_to(mymap)
    m = mymap._repr_html_()
    # Save the map as an HTML file
    # mymap.save("google_map_example.html")
    return render(req, 'map.html', {'profile': req.session['patientprofile'], 'address': address, 'lat': lat, 'lng': lng, 'mymap': m})
