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
from collections import namedtuple
from . import emails
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

    main_email = request.session['email']
    company_jobs_docs = web_db.collection(u'jobs').where(u'email', u'==', main_email).get()
    company_jobs_ids = [job.reference.id for job in company_jobs_docs]
    # print(f'1 = {company_jobs_ids}')
    print(main_email,company_jobs_ids)
    job_docs = web_db.collection('applications').get()
    print("job docs applications")
    job_docs = [(job.to_dict(), job.id) for job in job_docs]
    total_jobs = len(job_docs)
    print(job_docs)
    print(total_jobs)
    company_jobs: List[Tuple[Dict, str]] = []
    """
    company_jobs will contain data of all jobs posted by company. Each item will be a 
    tuple of (1)Job Dict & (2)job id
    """
    #itr = 0

    for job_id in company_jobs_ids:
        print(job_id)
        for i in range(total_jobs):
            if job_id == job_docs[i][1]:
                company_jobs.append(job_docs[i])
                print(company_jobs, job_id,i)

    print("company jobs")
    print(company_jobs)

    counts = {'APPLIED': 0, 'REJECTED': 0, 'ACCEPTED': 0}
    application = namedtuple('application', ['job_info',
                                                'cand_profile',
                                                'app_dict',
                                                'appid',
                                                'video_interview',
                                                'video_interview_score',
                                                'soft_skill_avg',
                                                'subject_skill_avg'
                                                ]
                                )
    job_apps = []
    # print(company_jobs)

    for job, job_id in company_jobs:
        print("fetching applicant ",job_id)
        # get all applicant documents for a particular job
        applicants = web_db.collection('applications').document(job_id).collection('applicants').get()
        job_info = web_db.collection('jobs').document(job_id).get().to_dict()
        job_info['id'] = job_id


        questions = web_db.collection(u'users').document(main_email).collection(
            u'packages').document(job_info['packageId']).collection(u'questions').get()

        vid_interview_score = True

        for applicant in applicants:
            
            app_info = applicant.to_dict()
            appid: str = applicant.reference.id + job_id
            print("applicant ",appid)
            if vid_interview_score:
                if 'video_interview_score' not in app_info.keys():
                    vid_interview_score = 0
                else:
                    total = 0
                    soft_skill_avg=[0,0,0,0,0]
                    subject_skill_avg=0
                    ss = 0
                    sbs = 0
                    scores = app_info['video_interview_score'].values()
                    print("scores ",scores)
                    try:
                        for score in scores:
                            if isinstance(score, list):
                                soft_skill_avg = [soft_skill_avg[i] + int(score[i]) for i in range(len(soft_skill_avg))] 
                                ss+=1
                                print(soft_skill_avg,ss)
                            else:
                                subject_skill_avg+=int(score)
                                sbs+=1
                        print("taking average ",ss,sbs)
                        if ss>0:
                            for i in range(len(soft_skill_avg)):
                                soft_skill_avg[i]=int(soft_skill_avg[i])//ss
                        if sbs>0:        
                            subject_skill_avg/=sbs

                        print("average is ",subject_skill_avg,soft_skill_avg)

                    except Exception as e:
                            print("list err ",e, score)

                    vid_interview_score = total
            
            print("vide interview score ", vid_interview_score)
            if app_info['status'] == 'INVITED':
                cand_profile = None

            else:
                cand_profile = web_db.collection('candidates').document(applicant.id).get().to_dict()
                if cand_profile is None:
                    continue
                try:
                    counts[app_info['status']] += 1
                except KeyError:
                    web_db.collection('applications').document(job_id).collection(
                        'applicants').document(applicant.id).delete()
                    continue

                # get profile dict of each candidate
                cand_profile['cand_id'] = applicant.id


                vid_interviews = []

                questions_dict = {}
                for ques in questions:
                    questions_dict[ques.id] = ques.reference.get().to_dict()

                # print(questions_dict)
                # sum_interview_score = 0
                count = 0

                try:
                    for ques_id, video in app_info['video_interview_links'].items():
                        try:
                            que: str = questions_dict[ques_id]['question']
                        except KeyError:
                            continue

                        # sum_interview_score += app_info
                        ques_vid = (que, video)
                        vid_interviews.append(ques_vid)
                except AttributeError:
                    vid_interviews = None


            app = application(job_info=job_info, cand_profile=cand_profile,
                                app_dict=app_info, appid=appid.replace('@', '').replace('.', ''),
                                video_interview=vid_interviews,video_interview_score=vid_interview_score,subject_skill_avg=round(subject_skill_avg,2),soft_skill_avg=soft_skill_avg)
            #print(app)
            print("\n\n\n\n\n\n")
            """
            app is a namedtuple(think of it like a immutable dict), with shown attributes, 
            to access an attribute of app, use: app.attribute_name, i.e. app.job_info
            """
            job_apps.append(app)
            #print("final job apps ",job_apps)


    #job_apps.sort(key=sort_key, reverse=True)
    unique_jobs = [(job.job_info['id'], job.job_info['post']) for job in job_apps]
    unique_jobs = list(set(unique_jobs))

    unique_jobs = [{'id': job[0], 'post': job[1]} for job in unique_jobs]
    # print(job_apps)
    smessage = """
        Congratulations! You are selected as the top performer for the position of {}.
        We all are looking forward to working with you and are
        certain that you are going to be a great fit for the team.
        """
    ssubject = 'Hooray! You have been selected for the job'

    rmessage = """
        Thank you for your interest in the position of {}.We received many promising applications and regret to inform you that we have decided to proceed with other candidates
        and will not take your application further.
        We wish you all the best in your job search and all the other future professional endeavours.
        """
    rsubject = 'Sorry, Please Try again later.'

    return render(request, 'recruiter/candidates.html',
                    {'job_apps': job_apps, 'counts': counts, 'smessage': smessage,
                    'ssubject': ssubject, 'rmessage': rmessage, 'rsubject': rsubject,
                    'unique_jobs': unique_jobs,'company_name':request.session['cname'],'name':request.session['name']
                    }
                    )


        # except:
        #     return render(request, 'recruiter/candidates.html',
        #                   {'role': request.session['role'], 'name': request.session['name'], 'new_user': 'True',
        #                    'appcount': 0,
        #                    'company_name': request.session['cname'],
        #                    'account_type': account_type,
        #                    'notifications': notifications,
        #                    'unique_jobs': unique_jobs,
        #                    })



def view_interview(request, jid, candidate_id):

    application_dict = web_db.collection('applications').document(jid).collection(
        'applicants').document(candidate_id).get().to_dict()
    job_doc = web_db.collection('jobs').document(jid).get().to_dict()

    application_dict['jid'] = jid
    application_dict['candidate_id'] = candidate_id

    questions_doc = web_db.collection(u'users').document(job_doc['email']).collection(u'packages').document(
        job_doc['packageId']).collection(u'questions').get()
    que = []
    for q in questions_doc:
        que.append(q.to_dict())

    print(que)

    if 'video_interview_score' not in application_dict.keys():
        grades = dict()
        for ques in que:
            grades[ques['id']] = None

        web_db.collection('applications').document(jid).collection(
            'applicants').document(candidate_id).update({'video_interview_score': grades})
        application_dict['video_interview_score'] = grades

    # if 'video_interview_comments' not in application_dict.keys():
    #     comments = dict()
    #     for ques in que:
    #         comments[ques['id']] = None

    #     web_db.collection('applications').document(jid).collection(
    #         'applicants').document(candidate_id).update({'video_interview_comments': comments})
    #     application_dict['video_interview_comments'] = comments

    if 'video_interview_links' not in application_dict.keys():
        links = dict()
        for ques in que:
            links[ques['id']] = None

        web_db.collection('applications').document(jid).collection(
            'applicants').document(candidate_id).update({'video_interview_links': links})
        application_dict['video_interview_links'] = links

    # print(application_dict['video_interview_grades'])
    questions = []
    for ques in que:
        question_dict = dict()
        question_dict['question'] = ques['question']
        question_dict['id'] = ques['id']
        question_dict['video'] = application_dict['video_interview_links'].get(ques['id'], None)
        # print(question_dict['video'])
        question_dict['grade'] = application_dict['video_interview_score'].get(ques['id'], None)

        if question_dict['grade'] is None:
            question_dict['grade'] = 0

        #question_dict['comment'] = application_dict['video_interview_comments'].get(ques['id'], None)
        questions.append(question_dict)

    questions_length = len(questions)

    # 'ocean' radar data
    job_info = web_db.collection('jobs').document(jid).get().to_dict()
    job_info['id'] = jid

    cand_profile = web_db.collection('candidates').document(candidate_id).get().to_dict()

    app_info = web_db.collection('applications').document(jid).collection('applicants').document(
        candidate_id).get().to_dict()

    appid = candidate_id + jid
    application = namedtuple('application', ['job_info',
                                                            'cand_profile',
                                                            'app_dict',
                                                            'appid'])
    #skills_score = app_info['skills_score']
    # print(skills_score)
    app = application(job_info=job_info, cand_profile=cand_profile, app_dict=app_info,
                        appid=appid.replace('@', '').replace('.', ''))

    # job_apps = [app]
    # print(job_apps[0].skills_score)
    print(questions)
    return render(request, 'recruiter/viewinterview.html',
                    {'application_dict': application_dict, 'questions': questions,
                    'questions_length': questions_length, 
                    'name': request.session['name'],
                    'company_name': request.session['cname'],
                        'job_app': app,
                    })

    # except Exception as e:
    #     print(e)
    #     messages.error(request, 'Something went wrong! Try Again Later.')
        #return HttpResponseRedirect('/')




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
            
            print("hire mailing",c_email,name,post,sub,messg)
            emails.selmail(sub, messg, c_email, name, post)
            web_db.collection(u'applications').document(jid).collection(u'applicants').document(c_email).update({
                'status': "ACCEPTED"
            })
            print("mailed")
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
            print("rej mailing",jid,c_email)
            web_db.collection(u'applications').document(jid).collection(u'applicants').document(c_email).update({
                'status': "REJECTED"
            })
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