from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import db
from django.conf import settings
from string import ascii_lowercase, ascii_uppercase
from passlib.context import CryptContext
from datetime import datetime

# Database init
# Use a service account
cred = credentials.Certificate('./serviceAccountKey.json')

# Initialize the  web_app
web_app = firebase_admin.initialize_app(cred)
db = firestore.client()

# Powerful query not for developers
# docs = db.collection(u'users').get()
# for doc in docs:
#     new_pass = encrypt_password(db.collection(u'users').document(doc.id).get().to_dict()['password'])
#     db.collection(u'users').document(doc.id).set({u'password':new_pass}, merge=True)

def encrypt_password(password) -> str:
    # define a context for hashing
    # we can later hide this in some .env file
    context = CryptContext(schemes=['pbkdf2_sha256'],
                           default='pbkdf2_sha256',
                           pbkdf2_sha256__default_rounds=30000,
                           )
    return context.encrypt(password)


def check_password(user_provided, encrypted) -> bool:
    context = CryptContext(schemes=['pbkdf2_sha256'],
                           default='pbkdf2_sha256',
                           pbkdf2_sha256__default_rounds=30000,
                           )
    return context.verify(user_provided, encrypted)


def login(request):
    if request.method == "POST":

        try:
            email = request.POST.get('inputEmail')
            password = request.POST.get('inputPassword')

            if db.collection(u'users').document(email).get().exists:
                # user exists
                req = db.collection(u'users').document(email).get().to_dict()
                password_check = req['password']
                user_type = req['user_type']

                if check_password(password, password_check):
                    if user_type == 'Company':
                        request.session['name'] = req['name']
                        request.session['email'] = email
                        request.session['cname'] = req['company_name']
                        return HttpResponseRedirect('/recruiter/jobs')

                    if user_type == 'Admin':
                        request.session['name'] = req['name']
                        request.session['email'] = email
                        request.session['user_type'] = 'Admin'
                        return HttpResponseRedirect('/maintainer/mdashboard')

                    if user_type == 'Candidate':
                        request.session['name'] = req['name']
                        request.session['email'] = email
                        request.session['college'] = req['college']
                        return HttpResponseRedirect('/candidate/view_jobs')
                else:
                    messages.error(request, 'Invalid password')
                    return redirect('accounts:login')
            else:
                messages.error(request, 'Account does not exists')
        except:
            messages.error(request, 'Something went wrong! Try Again Later.')
    return render(request, 'accounts/login.html')


def recruiter_signup(request):
    if request.method == "POST":
        try:
            email = request.POST.get('inputEmail').strip()
            password = request.POST.get('inputPassword').strip()
            name = request.POST.get('name').strip()
            cname = request.POST.get('cname').strip()
            position = request.POST.get('inlineRadioOptions').strip()
            password1 = encrypt_password(password)
            print(email,password,name,cname,position,password1)
            if not db.collection(u'users').document(email).get().exists:
                request.session['email'] = email
                request.session['cname']=cname
                request.session['name']=name
                db.collection(u'users').document(email).set({
                    u'name': name,
                    u'company_name': cname,
                    u'password': password1,
                    u'position': position,
                    u'user_type': 'Company',
                    u'timestamp': datetime.now()
                })

                db.collection(u'users').document(email).collection(
                    u'packages').document(u'sample').set({u'id': 'sample'})
                sample_questions = ['Tell us about your education.', 'What kind of salary do you expect?',
                                    'What makes you passionate about this work?','What can you tell me about our company?',
                                    'Why did you leave your last job?']

                for ques in sample_questions:
                    ques_ref= db.collection(u'users').document(email).collection(
                            u'packages').document(u'sample').collection('questions').document()
                    ques_ref.set({
                        u'id' : ques_ref.id,
                        u'type' : 'SoftSkills',
                        u'question' : ques
                    })

                messages.success(request, 'Signup completed successfully.')
                return render(request, 'recruiter/jobs.html')

            else:
                messages.error(request, 'Email already exists.Proceed to login')
                return render(request, 'accounts/login.html')
        except:
            messages.error(request, 'Something went wrong! Try Again Later.')
    return render(request, 'accounts/recruiter_signup.html')

def candidate_signup(request):
    if request.method == "POST":
        try:
            email = request.POST.get('inputEmail').strip()
            password = request.POST.get('inputPassword').strip()
            name = request.POST.get('name').strip()
            college = request.POST.get('college').strip()
            password1 = encrypt_password(password)

            if not db.collection(u'users').document(email).get().exists:
                request.session['email'] = email
                request.session['college']=college
                request.session['name']=name
                db.collection(u'users').document(email).set({
                    u'name': name,
                    u'college': college,
                    u'password': password1,
                    u'user_type': 'Candidate',
                    u'timestamp': datetime.now()
                })

                messages.success(request, 'Signup completed successfully.')
                return render(request, 'candidate/dashboard.html')
            else:
                messages.error(request, 'Email already exists.Proceed to login')
                return render(request, 'accounts/login.html')
        except:
            messages.error(request, 'Something went wrong! Try Again Later.')
    return render(request, 'accounts/candidate_signup.html')

def logout(request):
    request.session.flush()
    return render(request, 'AIP/index.html')
