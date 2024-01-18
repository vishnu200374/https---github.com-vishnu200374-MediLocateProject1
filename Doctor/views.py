from django.shortcuts import render, redirect
from .models import DocRegistration, Reportupload
from Patient.models import Requests, Patienthistory
from django.contrib import messages
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from django.conf import settings
from django.core.mail import send_mail
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64
from .aesencrypt import encrypt, decrypt
from .rsa import encrypt_message, decrypt_message, generate_keys


# templates
INDEXPAGE = "index.html"
DOCSIGNUPPAGE = "docsignup.html"
DOCSIGNINPAGE = "docsignin.html"
DOCHOMEPAGE = "dochome.html"
VIEWAPPOINTMENTSPAGE = "viewappointments.html"
REPORTVIEWPAGE = "reportview.html"
UPLOADREPORTPAGE = "uploadreport.html"
VIEWFILESPAGE = "viewfiles.html"
VIEWREPORTSPAGE = "viewreports.html"
# SENDKEYPAGE = "sendkey.html"
# Create your views here.


def index(req):
    # DocRegistration.objects.all().delete()
    return render(req, INDEXPAGE)


def docsignup(req):
    if req.method == "POST":
        username = req.POST['username']
        useremail = req.POST['useremail']
        password = req.POST['password']
        confirmpassword = req.POST['confirmpassword']
        department = req.POST['department']
        address = req.POST['address']
        profile = req.FILES['profile']
        profilename = profile.name
        hospitalname = req.POST['hospitalname']
        hospitaladdress = req.POST['hospitaladdress']

        if password == confirmpassword:
            data = DocRegistration.objects.filter(
                useremail=useremail, password=password).exists()
            if data:
                messages.info(
                    req, "Account already exist with these credentials")
                return redirect("docsignin")
            dc = DocRegistration(username=username, useremail=useremail, password=password,
                                 department=department, address=address.lower(), profile=profile, profilename=profilename, hospitalname=hospitalname, hospitaladdress=hospitaladdress)
            dc.save()
            messages.success(req, "Registration Success")
            return redirect("docsignin")
        else:
            messages.error(req, "password & Confirm password are not matching")
            return render(req, DOCSIGNUPPAGE)
    return render(req, DOCSIGNUPPAGE)


def docsignin(req):
    if req.method == "POST":
        useremail = req.POST['useremail']
        password = req.POST['password']
        dc = DocRegistration.objects.filter(
            useremail=useremail, password=password).exists()
        if dc:
            pro = DocRegistration.objects.filter(
                useremail=useremail, password=password)
            profilename = [i.profilename for i in pro][0]
            req.session['docprofile'] = profilename
            req.session['docemail'] = useremail
            return render(req, DOCHOMEPAGE, {'profile': req.session['docprofile']})
        messages.info(req, "Doctor account does not exist")
        return render(req, DOCSIGNINPAGE)
    return render(req, DOCSIGNINPAGE)


def viewappointments(req):
    dc = Requests.objects.filter(doctoremail=req.session['docemail'])
    return render(req, VIEWAPPOINTMENTSPAGE, {'profile': req.session['docprofile'], 'dc': dc})


def reportview(req, id, reqid):
    print(reqid)
    dc = Patienthistory.objects.filter(useremail=req.session['useremail'])
    return render(req, REPORTVIEWPAGE, {'profile': req.session['docprofile'], 'dc': dc, 'pid': reqid})


def uploadreport(req, pid):
    dc = [i.patientemail for i in Requests.objects.filter(reqid=pid)]
    return render(req, UPLOADREPORTPAGE, {'profile': req.session['docprofile'], 'dc': dc[0], 'reqid': pid})


def fileupload(req):
    if req.method == "POST":

        reqid = req.POST['reqid']
        useremail = req.POST['useremail']
        myfile = req.FILES['myfile']
        filename = myfile.name
        content = myfile.read()

        secret_key = b'secret_key_16bytes'

        # Original data
        data = content
        private_key, public_key = generate_keys()
        message = str(content)
        print(message)
        encrypted_data = encrypt_message(message, public_key)
        # Encrypt data
        aesencrypted_data = encrypt(encrypted_data, secret_key)
        print(f"Encrypted Data: {encrypted_data}")
        # Decrypt data
        aesdecrypted_data = decrypt(aesencrypted_data, secret_key)
        print(f"Decrypted Data: {aesdecrypted_data}")

        decrypted_message = decrypt_message(encrypted_data, private_key)
        print(decrypted_message)
        dc = Reportupload(
            reqid=reqid,
            filename=filename,
            myfile=myfile,
            patientemail=useremail,
            doctoremail=req.session['docemail'],
            filecontent=aesdecrypted_data,
            key=secret_key
        )
        dc.save()

        return redirect("viewreports")

    # dc = Reportupload.objects.filter(doctoeremail=req.session['docemail'],patientemail = useremail)
    # return render(req,VIEWFILESPAGE,{'profile':req.session['docprofile']})


def viewreports(req):
    dc = Reportupload.objects.filter(
        doctoremail=req.session['docemail'], patientemail=req.session['useremail'])
    return render(req, VIEWFILESPAGE, {'profile': req.session['docprofile'], 'dc': dc})


def sendkey(req, reqid):
    print(reqid)
    dc = [(i.reqid, i.filename, i.myfile, i.patientemail, i.doctoremail,
           i.filecontent, i.key) for i in Reportupload.objects.filter(reqid=reqid)]
    print(dc)
    subject = "No reply"
    cont = 'The private key to decrypt file.'

    KEY = dc[0][6]
    print(KEY)
    m1 = "This message is automatic generated so dont reply to this Mail"
    m2 = "Thanking you"
    m3 = "Regards"
    m4 = "Cloud Service Provider."
    # Email = useremails
    print(KEY)
    email_from = settings.EMAIL_HOST_USER
    # recipient_list = [Email]
    # text = cont + '\n' + KEY + '\n' + m1 + '\n' + m2 + '\n' + m3 + '\n' + m4
    # send_mail(subject, text, email_from, recipient_list,fail_silently=False,)

    messages.success(req, "Key Sent successfully")
    return redirect("viewreports")
