from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
import firebase_admin
import json
from firebase_admin import credentials
from firebase_admin import firestore
from django.conf import settings
from string import ascii_lowercase, ascii_uppercase
from django.views.decorators.csrf import csrf_exempt 
from django.core.files.storage import FileSystemStorage
import sys
import os
import csv



db = firestore.client()

# Create your views here.

# General Stats
def mdashboard(request):
    try:
        name = request.session['name']
        email = request.session['email']
        total_companies=0
        total_candidates=0
        total_jobs_posted=0
        total_applied_candidates=0
        total_accepted_candidates=0
        total_rejected_candidates=0
        users = db.collection('users').get()
        for user in users:
            #print(user.id)
            temp=db.collection('users').document(user.id).get().to_dict()
            if temp['user_type']=='Candidate':
                total_candidates+=1

            if temp['user_type']=='Company':
                total_companies+=1
                temp1 = db.collection('jobs').where(u'email', u'==', user.id).stream()
                for t in temp1:
                    total_jobs_posted+=1
                    temp2 = db.collection('applications').document(t.id).collection('applicants').where(u'status', u'==', 'APPLIED').stream()
                    for t1 in temp2:
                        total_applied_candidates+=1

                    temp3 = db.collection('applications').document(t.id).collection('applicants').where(u'status', u'==', 'ACCEPTED').stream()
                    for t2 in temp3:
                        total_accepted_candidates+=1

                    temp4 = db.collection('applications').document(t.id).collection('applicants').where(u'status', u'==', 'REJECTED').stream()
                    for t3 in temp4:
                        total_rejected_candidates+=1

        print(total_companies,total_candidates,total_jobs_posted,total_applied_candidates,total_rejected_candidates,total_accepted_candidates)
        return render(request,'maintainer/mdashboard.html',{'name':name,'total_companies':total_companies,'total_candidates':total_candidates,'total_jobs_posted':total_jobs_posted,'total_applied_candidates':total_applied_candidates,'total_rejected_candidates':total_rejected_candidates,'total_accepted_candidates':total_accepted_candidates})
    except:
        messages.error(request, 'Something went wrong! Try Again Later.')
    return HttpResponseRedirect('/')

# User management, Signup,remove,edit,etc on users db recruiter and campus
@csrf_exempt
def users(request):
    """
    User Management tab.
    Lists all users of the website.
    Option to search or bulk delete users from the database.
    """
    try:
        if request.session['user_type'] == 'Admin':
            name = request.session['name']
            users = {}
            docs = db.collection(u'users').get()
            for doc in docs:
                users[doc.id] = doc.to_dict()
                if 'user' not in users[doc.id]:
                    users[doc.id]['user']="-"
            if request.method == "POST":
                if request.POST.get('req').strip() == 'delete':
                    emails = request.POST.getlist('deletion[]')
                    if len(emails) != 0:
                        for email in emails:
                            db.collection(u'users').document(email).delete()
                    return JsonResponse({"success": "true"})
            return render(request,'maintainer/users.html',{'name':name,'users':users})
    except:
        messages.error(request, 'Something went wrong! Try Again Later.')
        return redirect('accounts:login')


@csrf_exempt
def post_question(request):
    """
    Post questions tab.
    Post questions to the database. Each question has a "type" associated with it.
    Also has an option to uplod from CSV files. Only works if the file follows the format of ("question","type") and has to be a csv file
    """
    try:
        if request.session['user_type'] == 'Admin':
            name = request.session['name']
            questions = {}
            docs = db.collection(u'questions').get()
            for doc in docs:
                questions[doc.id] = doc.to_dict()
                if 'question' not in questions[doc.id]:
                    questions[doc.id]['question']="-"
            if request.method == "POST":

                # File upload

                #Adding Questions through the Submit button i.e POST method
                quess=request.POST.get('post-questions').strip()
                qtypee=request.POST.get('qtype').strip()
                doc_ref = db.collection(u'questions').document()
                doc_ref.set({
                        u'id':doc_ref.id,
                        u'question':quess,
                        u'type': qtypee,
                    })
                return redirect(post_question)
            return render(request,'maintainer/post_question.html',{'name':name,'questions':questions})
    except:
        messages.error(request, 'Something went wrong! Try Again Later.')
        return redirect('accounts:login')

@csrf_exempt
def post_csv_question(request):
    try:
        if request.session['user_type'] == 'Admin':
            if request.method == 'POST':
                if 'post_csv_question' in request.FILES.keys():
                    ALLOWED_FILES = ["csv"]
                    doc_reft = db.collection(u'questions')
                    myfile = request.FILES['post_csv_question']
                    file_data = myfile.read().decode("utf-8")

                    csvfilename = myfile.name
                    name,ext = csvfilename.split('.')

                    if ext in ALLOWED_FILES:
                        lines = file_data.split("\n")

                        for line in lines[1:]:
                            comma = line.rfind(',')
                            ques,ques_type = line[:comma].strip(), line[comma+1:].strip()

                            if ques == '' or ques_type == '':
                                continue

                            doc_reft.add({
                                    u'question':ques,
                                    u'type': ques_type,
                                })
                    return redirect(post_question)
    except:
        messages.error(request, 'Something went wrong! Try Again Later.')
        return redirect('accounts:login')

#View for Ajax call to edit a question
@csrf_exempt
def edit_question(request):
    try:
        if request.session['user_type'] == 'Admin':
            if request.method == "POST":
                questionid = request.POST.get('questionid').strip()
                edquestion = request.POST.get('equestion').strip()
                edquestiontyp = request.POST.get('eqtype').strip()
                doc_refe = db.collection(u'questions').document(questionid)
                doc_refe.set({
                    u'id':questionid,
                    u'question':edquestion,
                    u'type':edquestiontyp,
                })
                return JsonResponse({"success": "true"})
            else:
                return JsonResponse({"success": "false"})
    except:
        messages.error(request, 'Something went wrong! Try Again Later.')
        return redirect('accounts:login')
     
#View for Ajax call to delete a question
@csrf_exempt
def delete_question(request):
    try:
        if request.session['user_type'] == 'Admin':
            if request.method == "POST":
                questionss = request.POST.getlist('deletion[]')
                if len(questionss) != 0:
                    for questionn in questionss:
                        db.collection(u'questions').document(questionn).delete()
                return JsonResponse({"success": "true"})
            else:
                return JsonResponse({"success":"false"})
    except:
        messages.error(request, 'Something went wrong! Try Again Later.')
        return redirect('accounts:login')
