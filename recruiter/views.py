from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.contrib import messages
from django.views import View
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import credentials
from firebase_admin import db
from datetime import datetime
import shutil
import os
from random import randint

# Database init
# Use a service account

web_db = firestore.client()

# Create your views here.


def jobs(request):
    # try:
        main_email=request.session['email']

        if request.method == "POST":
            try:
                packageId = request.POST.get('userPackages').strip()
                post = request.POST.get('post').strip()
                job_description = request.POST.get('jobdesc').strip()
                key_responsibility = request.POST.get('keyresp').strip()
                tskill = request.POST.getlist('tskill')
                sskill = request.POST.getlist('sskill')
                other = request.POST.getlist('other')
                bond = request.POST.get('bond').strip()
                salary = request.POST.get('salary').strip()
                add_detail = request.POST.get('adddetail').strip()
                place = request.POST.get('place').strip()
                joining_date = request.POST.get('startdate').strip()
                deadline = request.POST.get('deadline').strip()
                status = 'Opened'
                # jobid = main_email + '$' + post + '$' + datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                #print(company_name,post,job_description,tskill,sskill,other,bond,salary,add_detail,status,jobid,place,joining_date,deadline,key_responsibility)
                doc_ref = web_db.collection(u'jobs').document()
                doc_ref.set({
                    u'post': post,
                    u'job_description': job_description,
                    u'key_responsibility': key_responsibility,
                    u'place': place,
                    u'tskill': tskill,
                    u'sskill': sskill,
                    u'other': other,
                    u'start_date': joining_date,
                    u'deadline': deadline,
                    u'bond': bond,
                    u'salary': salary,
                    u'add_detail': add_detail,
                    u'status': status,
                    u'email': main_email,
                    u'packageId': packageId,
                    u'timestamp':datetime.now()
                })


                messages.success(request, 'Job posted successfully.')
            except:
                messages.error(request, 'Something went wrong! Try Again Later.')

        # get jobs data
        docs = web_db.collection(u'jobs').where(u'email', u'==', main_email).get()
        jobs = []
        open_count = 0
        for doc in docs:
            stat = doc.to_dict()['status']
            deadline = doc.to_dict()['deadline']
            if stat == 'Opened':
                if datetime.strptime(deadline, '%Y-%m-%d') < datetime.today():
                    web_db.collection(u'jobs').document(doc.id).set({u'status': 'Closed'}, merge=True)
                    doc.to_dict()['status'] = 'Closed'
                else:
                    open_count += 1
            temp = doc.to_dict()
            temp.update({'id': doc.id})
            jobs.append(temp)
        user_packages_docs = web_db.collection(u'users').document(main_email).collection(u'packages').get()
        user_packages = []
        for doc in user_packages_docs:
            user_packages.append(doc.id)

        close_count = len(jobs) - open_count
        if not jobs:
            return render(request, 'recruiter/jobs.html',
                            { 'new_user': 'True', 'name': request.session['name'],
                            'jc': 0, 'oc': 0, 'cc': 0, 'user_packages': user_packages})
        else:
            return render(request, 'recruiter/jobs.html',
                            { 'new_user': 'False', 'jobs': jobs,
                            'name': request.session['name'], 'jc': len(jobs),
                            'oc': open_count, 'cc': close_count, 'user_packages': user_packages})

    # except:
    #     messages.error(request, 'Something went wrong! Try Again Later.')
    #     return HttpResponseRedirect('/')


def deletepost(request):
    try:
        # From post job form
        if request.method == "POST":
            main_email = request.session['email']

            try:
                id = request.POST.get('id').strip()
                job_doc = web_db.collection(u'jobs').document(id).get()
                job_post = job_doc.get('post')
                web_db.collection(u'jobs').document(id).delete()
                messages.success(request, 'Post deleted successfully.')

                return JsonResponse({"success": "true"})
            except:
                messages.error(request, 'Something went wrong! Try Again Later.')
                return JsonResponse({"success": "false"})

    except:
        messages.error(request, 'Something went wrong! Try Again Later.')
        return HttpResponseRedirect('AIP/404.html')


def candidates(request):
    # try:
        
        return render(request, 'recruiter/candidates.html',{ 'name': request.session['name'], 'new_user': 'True',
                            'appcount': 0})
            # try:
                
            #     company_jobs_docs = web_db.collection(u'jobs').where(u'email', u'==', main_email).get()
            #     company_jobs = []

            #     job_docs = db.reference('JOBS APPLICATIONS/', config.android_app).get()
            #     job_apps = []
            #     for doc in company_jobs_docs:
            #         company_jobs.append(doc.id.strip())

            #     applied = 0
            #     rejected = 0
            #     recruited = 0

            #     for jobs_doc in job_docs.items():
            #         if jobs_doc[0].strip() in company_jobs:
            #             for item in jobs_doc[1].items():
            #                 job_app_dict = item[1]
            #                 job_app_dict['jid'] = jobs_doc[0].strip()
            #                 job_app_dict['appid'] = item[0].strip() + jobs_doc[0].strip()
            #                 job_app_dict['candidate_id'] = item[0].strip()

            #                 job_info_doc = web_db.collection(u'jobs').document(jobs_doc[0].strip()).get()
            #                 job_app_dict['job_info'] = job_info_doc.to_dict()

            #                 applied += 1
            #                 if job_app_dict['status'] == 'REJECTED':
            #                     rejected += 1
            #                 elif job_app_dict['status'] == 'ACCEPTED':
            #                     recruited += 1
            #                 job_apps.append(job_app_dict)
            #                 smessage = """
            # Congratulations! You are selected as the top performer for the position of {} to receive an offer to join Apli.ai.
            # We all are looking forward to working with you and are
            # certain that you are going to be a great fit for the team.

            #                 """
            #                 rmessage = """
            # Thank you for your interest in the position of {} at Apli.ai.We received many promising applications and regret to inform you that we have decided to proceed with other candidates
            # and will not take your application further.
            # We wish you all the best in your job search and all the other future professional endeavours.

            #                 """
            #     return render(request, 'recruiter/candidates.html',
            #                 {'role': request.session['role'], 'name': request.session['name'],
            #                 'new_user': 'False',
            #                 'applied': applied, 'rejected': rejected,
            #                 'recruited': recruited, 'job_apps': job_apps, 'smessage': smessage,
            #                 'ssubject': 'Hooray! You have been selected for the job', 'rmessage': rmessage,
            #                 'rsubject': 'Sorry, Please Try again later.'})
            # except:
            #     return render(request, 'recruiter/candidates.html',
            #                 {'role': request.session['role'], 'name': request.session['name'], 'new_user': 'True',
            #                 'appcount': 0})
    
    # except:
    #     messages.error(request, 'Something went wrong! Try Again Later.')
    #     return HttpResponseRedirect('/')


def view_interview(request, jid, candidate_id):
    try:
        # application_dict = db.reference('JOBS APPLICATIONS/' + jid + '/' + candidate_id + '/', config.android_app).get()
        # application_dict['jid'] = jid
        # application_dict['candidate_id'] = candidate_id

        # questions = []
        # counter = 1
        # for doc in range(len(application_dict['questions']) - 1):
        #     question_dict = {}
        #     question_dict['question'] = application_dict['questions'][counter]
        #     question_dict['video'] = application_dict['video_interview_links'][counter]
        #     question_dict['grade'] = application_dict['grades'][counter]
        #     question_dict['comment'] = application_dict['comments'][counter]

        #     questions.append(question_dict)
        #     counter = counter + 1

        # questions_length = len(questions)

        return render(request, 'recruiter/viewinterview.html',{'name': request.session['name']})

    except:
        messages.error(request, 'Something went wrong! Try Again Later.')
        return HttpResponseRedirect('/')


def hiremail(request):
    try:
        if request.method == "POST":
            email=request.session['email']
            jid = request.POST.get('jid').strip()
            candidate_id = request.POST.get('candidate_id').strip()

            c_email = request.POST.get('c_email').strip()
            name = request.POST.get('c_name').strip()
            post = request.POST.get('c_post').strip()
            sub = request.POST.get('c_sub').strip()
            messg = request.POST.get('c_messg').strip()
            messg = messg.format(post)
            # db.reference('JOBS APPLICATIONS/' + jid + '/' + candidate_id + '/', config.android_app).update({
            #     u'status': u'ACCEPTED'
            # })
            emails.selmail(sub, messg, c_email, name, post)

            return JsonResponse({"success": "true"})
    except:
        messages.error(request, 'Something went wrong! Try Again Later.')
        return JsonResponse({"success": "true"})


def rejmail(request):
    try:
        if request.method == "POST":
            jid = request.POST.get('jid').strip()
            candidate_id = request.POST.get('candidate_id').strip()
            c_email = request.POST.get('c_email').strip()
            name = request.POST.get('c_name').strip()
            post = request.POST.get('c_post').strip()
            sub = request.POST.get('c_sub').strip()
            messg = request.POST.get('c_messg').strip()
            messg = messg.format(post)
            # db.reference('JOBS APPLICATIONS/' + jid + '/' + candidate_id + '/', config.android_app).update({
            #     u'status': u'REJECTED'
            # })
            emails.rejmail(sub, messg, c_email, name, post)
            return JsonResponse({"success": "true"})
    except:
        messages.error(request, 'Something went wrong! Try Again Later.')
        return JsonResponse({"success": "true"})


def question(request):
    # try:
        main_email=request.session['email']
        user_packages_docs = web_db.collection(u'users').document(main_email).collection(
            u'packages').get()
        user_packages = []
        for doc in user_packages_docs:
            user_packages.append(doc.id)

        user_questions_docs = web_db.collection(u'users').document(main_email).collection(
            u'packages').document('sample').collection(
            u'questions').get()
        user_questions = []
        for doc in user_questions_docs:
            user_questions.append(doc.to_dict())

        built_in_questions_docs = web_db.collection(u'questions').where(u'type', u'==', u'SoftSkills').get()
        built_in_questions = []
        for doc in built_in_questions_docs:
            built_in_questions.append(doc.to_dict())

        return render(request, 'recruiter/question.html',
                        { 'user_questions': user_questions,
                        'built_in_questions': built_in_questions,
                        'user_packages': user_packages, 'name': request.session['name']})

    # except:
    #     messages.error(request, 'Something went wrong! Try Again Later.')
    #     return HttpResponseRedirect('/')


def addpackage(request):
    # try:
        main_email=request.session['email']
        # From post job form
        if request.method == "POST":
            try:
                packageName = request.POST.get('packageName').strip()
                question = request.POST.get('question').strip()
                questionType = request.POST.get('questionType').strip()
                web_db.collection(u'users').document(main_email).collection(
                    u'packages').document(packageName).set({u'id': packageName})
                doc_ref = web_db.collection(u'users').document(main_email).collection(
                    u'packages').document(packageName).collection(
                    u'questions').document()
                web_db.collection(u'users').document(main_email).collection(
                    u'packages').document(packageName).collection(
                    u'questions').document(doc_ref.id).set({
                    u'id': doc_ref.id,
                    u'question': question,
                    u'type': questionType,
                })
                return JsonResponse({"success": "true"})
            except:
                return JsonResponse({"success": "false"})

    # except:
    #     messages.error(request, 'Something went wrong! Try Again Later.')
    #     return HttpResponseRedirect('/')


def changepackage(request):
    # try:
        main_email=request.session['email']
        if request.method == "POST":
            try:
                packageName = request.POST.get('packageName').strip()

                user_questions_docs = web_db.collection(u'users').document(main_email).collection(
                    u'packages').document(packageName).collection(
                    u'questions').get()
                user_questions = []
                for doc in user_questions_docs:
                    user_questions.append(doc.to_dict())

                return JsonResponse({"user_questions": user_questions})
            except:
                return JsonResponse({"success": "false"})

    # except:
    #     messages.error(request, 'Something went wrong! Try Again Later.')
    #     pass


def loadquestions(request):
    # try:
        main_email=request.session['email']
        if request.method == "POST":
            try:
                questionType = request.POST.get('questionType').strip()

                built_in_questions_docs = web_db.collection(
                    u'questions').where(u'type', u'==', questionType).get()
                built_in_questions = []
                for doc in built_in_questions_docs:
                    built_in_questions.append(doc.to_dict())

                return JsonResponse({"built_in_questions": built_in_questions})
            except:
                return JsonResponse({"success": "false"})

    # except:
    #     messages.error(request, 'Something went wrong! Try Again Later.')
    #     pass


def addquestion(request):
    # try:
        main_email=request.session['email']

        if request.method == "POST":
            try:
                packageName = request.POST.get('packageName').strip()
                question = request.POST.get('question').strip()
                questionType = request.POST.get('questionType').strip()

                doc_ref = web_db.collection(u'users').document(main_email).collection(
                    u'packages').document(packageName).collection(
                    u'questions').document()
                web_db.collection(u'users').document(main_email).collection(
                    u'packages').document(packageName).collection(
                    u'questions').document(doc_ref.id).set({
                    u'id': doc_ref.id,
                    u'question': question,
                    u'type': questionType,
                })
                return JsonResponse({"success": "true"})
            except:
                return JsonResponse({"success": "false"})
    # except:
    #     messages.error(request, 'Something went wrong! Try Again Later.')
    #     return HttpResponseRedirect('/')


def getPackages(request):
    # try:
        main_email = request.session['email']

        if request.method == "GET":
            try:
                user_packages_docs = web_db.collection(u'users').document(main_email).collection(
                    u'packages').get()
                user_packages = []
                for doc in user_packages_docs:
                    user_packages.append(doc.id)
                return JsonResponse({"user_packages": user_packages})
            except:
                return JsonResponse({"success": "false"})

    # except:
    #     messages.error(request, 'Something went wrong! Try Again Later.')
    #     return HttpResponseRedirect('/')


def deletequestion(request):
    # try:
        main_email=request.session['email']
        if request.method == "POST":
            try:
                id = request.POST.get('id').strip()
                packageName = request.POST.get('packageName').strip()
                web_db.collection(u'users').document(main_email).collection(
                    u'packages').document(packageName).collection(
                    u'questions').document(id).delete()
                return JsonResponse({"success": "true"})
            except:
                messages.error(request, 'Something went wrong! Try Again Later.')
                return JsonResponse({"success": "false"})

    # except:
    #     messages.error(request, 'Something went wrong! Try Again Later.')
    #     return HttpResponseRedirect('/')