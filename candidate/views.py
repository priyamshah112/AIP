from django.shortcuts import render
from django.http import HttpResponse

def view_jobs(request):
    return render(request,'candidate/view_jobs.html')

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import db
from django.conf import settings
from . import emails
from string import ascii_lowercase, ascii_uppercase
from passlib.context import CryptContext
from datetime import datetime

# Database init
# Use a service account
cred = credentials.Certificate('./serviceAccountKey.json')

# Initialize the  web_app
web_app = firebase_admin.initialize_app(cred)
db = firestore.client()


#  Initialize the android_app


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


def reachus(request):
    if request.method == "POST":
        try:
            name = request.POST.get('emp_name').strip()
            workplace = request.POST.get('company_name').strip()
            work_email = request.POST.get('company_email').strip()
            user_type = request.POST.get('user_type').strip()

            if db.collection(u'users').document(work_email).get().exists:
                messages.info(request, 'Account with this email already exists')
                return redirect('accounts:login')

            if db.collection(u'reachus').document(work_email).get().exists:
                messages.info(request, 'Your request has been already submitted')
                return redirect('accounts:login')

            if request.POST.get('emp_num').strip() == '':
                db.collection(u'reachus').document(work_email).set({
                    u'name': name,
                    u'workplace': workplace,
                    u'user_type': user_type
                })
                contact = '-'
            else:
                contact = request.POST.get('emp_num').strip()
                db.collection(u'reachus').document(work_email).set({
                    u'name': name,
                    u'workplace': workplace,
                    u'user_type': user_type,
                    u'contact': contact
                })
            email_from = settings.EMAIL_HOST_USER
            emails.mail(email_from, work_email)
            emails.mail2(workplace, work_email, name, str(contact), user_type)
            messages.success(request, 'Form submitted successfully, you will be contacted soon.')
        except:
            messages.error(request, 'Something went wrong! Try Again Later.')
    return render(request, 'accounts/reachus.html')


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

                # if check_password(password, password_check):
                if user_type == 'Company':
                    role = req['role']
                    # session start
                    request.session['name'] = req['name']
                    request.session['email'] = email
                    request.session['cname'] = req['company_name']
                    request.session['position'] = req['position']

                    if role == 'Recruiter':
                        request.session['role'] = 'Recruiter'
                    if role == 'Interviewer':
                        request.session['role'] = 'Interviewer'
                        request.session['parent'] = req['parent']
                    if role == 'Librarian':
                        request.session['role'] = 'Librarian'
                        request.session['parent'] = req['parent']
                    if role == 'Staff':
                        request.session['role'] = 'Staff'
                        request.session['parent'] = req['parent']
                    return HttpResponseRedirect('/recruiter/dashboard')

                if user_type == 'Campus':
                    request.session['name'] = req['name']
                    request.session['email'] = email
                    request.session['cname'] = req['college']
                    request.session['user_type'] = 'Campus'
                    return HttpResponseRedirect('/campus/batch')

                if user_type == 'Admin':
                    request.session['name'] = req['name']
                    request.session['email'] = email
                    request.session['user_type'] = 'Admin'
                    return HttpResponseRedirect('/maintainer/mdashboard')
                else:
                    messages.error(request, 'Invalid password')
                    return redirect('accounts:login')
            else:
                messages.error(request, 'Account does not exists')
        except:
            messages.error(request, 'Something went wrong! Try Again Later.')
    return render(request, 'accounts/login.html')


def signup(request):
    if request.method == "POST":
        try:
            email = request.POST.get('inputEmail').strip()
            password = request.POST.get('inputPassword').strip()

            if not db.collection(u'users').document(email).get().exists:
                request.session['email'] = email
                request.session['password'] = password
                return render(request, 'accounts/step1.html')
            else:
                messages.error(request, 'Email already exists.Proceed to login')
        except:
            messages.error(request, 'Something went wrong! Try Again Later.')
    return render(request, 'accounts/signup.html')


def step1(request):
    if request.method == "POST":
        try:
            name = request.POST.get('name').strip()
            request.session['name'] = name
            return render(request, 'accounts/step2.html', {'name': name})
        except:
            messages.error(request, 'Something went wrong! Try Again Later.')
    return render(request, 'accounts/step1.html')


def step2(request):
    if request.method == "POST":
        try:
            cname = request.POST.get('cname').strip()
            request.session['cname'] = cname
            return render(request, 'accounts/step3.html', {'name': request.session['name'], 'cname': cname})
        except:
            messages.error(request, 'Something went wrong! Try Again Later.')
    return render(request, 'accounts/step2.html')


def step3(request):
    if request.method == "POST":
        try:
            position = request.POST.get('inlineRadioOptions').strip()
            email = request.session['email']
            password = encrypt_password(request.session['password'])
            name = request.session['name']
            cname = request.session['cname']
            db.collection(u'users').document(email).set({
                u'name': name,
                u'company_name': cname,
                u'password': password,
                u'position': position,
                u'role': 'Recruiter',
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
                   u'type' : 'BEHAVIORAL',
                   u'question' : ques
               })
            messages.success(request, 'Signup completed successfully.')
            emails.mail3(email)
            return render(request, 'accounts/login.html')
        except:
            messages.error(request, 'Something went wrong! Try Again Later.')
    return render(request, 'accounts/step3.html')


def campus_signup(request):
    if request.method == "POST":
        try:
            college_name = request.POST.get('cname').strip()
            email = request.POST.get('email').strip()
            password = encrypt_password(request.POST.get('password').strip())
            name = request.POST.get('uname').strip()

            if not db.collection(u'users').document(email).get().exists:
                db.collection(u'users').document(email).set({
                    u'name': name,
                    u'college': college_name,
                    u'password': password,
                    u'user_type': 'Campus',
                    u'timestamp': datetime.now()
                })
                messages.success(request, 'Signup completed successfully.')
            else:
                messages.info(request, 'Account already exists.')
            return render(request, 'accounts/login.html')
        except:
            messages.error(request, 'Something went wrong! Try Again Later.')
    return render(request, 'accounts/campus_signup.html')


def teamsignup(request, encodeddata):
    try:
        encodeddatareceived = "{}".format(encodeddata)
        pass_phrase = 'E7rtQhHyMPriyam'
        used = {' ', '\n'}
        key = []
        for c in pass_phrase.lower() + ascii_lowercase:
            if c not in used:
                key.append(c)
                used.add(c)
        key = ''.join(key)
        decode = {v: u for u, v in zip(ascii_lowercase, key)}
        list = encodeddatareceived.split('$')
        decodedrecmail = ''.join([decode.get(c, c) for c in list[1].lower()])
        decodedrole = ''.join([decode.get(c, c) for c in list[2].lower()])
        decodedinvmail = ''.join([decode.get(c, c) for c in list[3].lower()])
        recrmail = decodedrecmail
        invrole = decodedrole
        invimail = decodedinvmail
        params = {'recmail': decodedrecmail, 'role': decodedrole, 'invmail': decodedinvmail}

        if request.method == "POST":
            member_info = db.collection(u'users').document(request.POST.get('inputEmail')).get().to_dict()
            if member_info['status'] == 'inactive':
                recEmail = request.POST.get('recEmail').strip()
                inputEmail = request.POST.get('inputEmail').strip()
                password = encrypt_password(request.POST.get('inputPassword').strip())
                name = request.POST.get('name').strip()
                position = request.POST.get('inlineRadioOptions').strip()
                company_name = db.collection(u'users').document(recEmail).get().to_dict()['company_name']
                db.collection(u'users').document(inputEmail).update({
                    'status': 'active',
                    'position': position,
                    'name': name,
                    'password': password,
                    'company_name': company_name,
                    'user_type': 'Company',
                    u'timestamp': datetime.now()
                })
                messages.success(request,"Member signed up successfully.")
                return redirect('accounts:login')

            elif member_info['status'] == 'active':
                messages.error(request,"Account Already exists.")
                return render(request, 'accounts/member_signup.html',params)
    except:
        messages.error(request, 'Something went wrong! Try Again Later.')
    return render(request, 'accounts/member_signup.html', params)


def logout(request):
    request.session.flush()
    return render(request, 'apliai/index.html')


def forgot_password(request):
    if request.method == "POST":
        try:
            umail = request.POST.get('usermail').strip()
            if db.collection(u'users').document(umail).get().exists:
                emails.fmail(umail)
                messages.success(request,
                                 'An email with the password reset link has been sent to the email address specified.Please click on the reset link to reset your password.')
                return render(request, 'accounts/forgot_password.html')
            else:
                messages.error(request, 'There is no account associated with that email address.')
        except:
            import traceback
            traceback.print_exc()
            messages.error(request, 'Something went wrong! Try Again Later.')
    return render(request, 'accounts/forgot_password.html')


def reset_confirm(request, umail):
    usermail = "{}".format(umail)
    pass_phrase = 'E7rtQhHyMPriyam'
    used = {' ', '\n'}
    key = []
    for c in pass_phrase.lower() + ascii_lowercase:
        if c not in used:
            key.append(c)
            used.add(c)
    key = ''.join(key)
    decode = {v: u for u, v in zip(ascii_lowercase, key)}
    decmail = ''.join([decode.get(c, c) for c in usermail.lower()])
    global strmail
    strmail = decmail
    return render(request, 'accounts/reset_confirm_form.html')


def reset_password_successful(request):
    try:
        if request.method == "POST":
            password = encrypt_password(request.POST.get('password').strip())

            db.collection(u'users').document(strmail).set({
                u'password': password,
            }, merge=True)
        messages.success(request, "Password Reset Successfully")
        return render(request, 'accounts/login.html')
    except:
        messages.error(request, "Oops! Something Went Wrong. Please Try again later!")
    return redirect('accounts:login')