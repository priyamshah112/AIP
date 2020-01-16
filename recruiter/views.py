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
    if request.method == 'GET':

        main_email = request.session['email']
        company_jobs_docs = web_db.collection(u'jobs').where(u'email', u'==', main_email).get()
        company_jobs_ids = [job.reference.id for job in company_jobs_docs]
        # print(f'1 = {company_jobs_ids}')

        job_docs = web_db.collection('applications').get()

        job_docs = [(job.to_dict(), job.id) for job in job_docs]
        total_jobs = len(job_docs)

        company_jobs: List[Tuple[Dict, str]] = []
        """
        company_jobs will contain data of all jobs posted by company. Each item will be a 
        tuple of (1)Job Dict & (2)job id
        """
        itr = 0

        for job_id in company_jobs_ids:
            while itr < total_jobs and job_docs[itr][1] != job_id:
                itr += 1

            if itr >= total_jobs:
                break
            company_jobs.append(job_docs[itr])
            itr += 1

        # print(company_jobs)

        counts = {'APPLIED': 0, 'REJECTED': 0, 'ACCEPTED': 0}
        application = namedtuple('application', ['job_info',
                                                    'cand_profile',
                                                    'app_dict',
                                                    'appid',
                                                    'video_interview',
                                                    'video_resume',
                                                    'resume',
                                                    'video_interview_score',
                                                    ]
                                    )
        job_apps = []
        # print(company_jobs)

        for job, job_id in company_jobs:
            # print(job_id)
            # get all applicant documents for a particular job
            applicants = web_db.collection('applications').document(job_id).collection('applicants').get()
            job_info = web_db.collection('jobs').document(job_id).get().to_dict()
            job_info['id'] = job_id

            if job_info['applicat_req']['vid_interview']:
                questions = web_db.collection(u'users').document(main_email).collection(
                    u'packages').document(job_info['packageId']).collection(u'questions').get()

                vid_interview_score = True
            else:
                vid_interview_score = False

            for applicant in applicants:
                # print(job_id)
                app_info = applicant.to_dict()
                appid: str = applicant.reference.id + job_id

                if vid_interview_score:
                    if 'video_interview_grades' not in app_info.keys():
                        vid_interview_score = None
                    else:
                        total = 0
                        scores = app_info['video_interview_grades'].values()

                        for score in scores:
                            if score is None:
                                total = None
                                break
                            total += score

                        if isinstance(total, int) and len(scores) != 0:
                            total //= len(scores)

                        vid_interview_score = total

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

                if job_info['applicat_req']['vid_interview']:
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
                else:
                    vid_interviews = False

                if job_info['applicat_req']['vid_resume']:
                    vid_resume = app_info.get('vid_resume_link', None)
                else:
                    vid_resume = False

                if cand_profile is not None:
                    resume = cand_profile.get('pdfResume', None)
                else:
                    resume = None

                app = application(job_info=job_info, cand_profile=cand_profile, resume=resume,
                                    app_dict=app_info, appid=appid.replace('@', '').replace('.', ''),
                                    video_interview=vid_interviews, video_resume=vid_resume,
                                    video_interview_score=vid_interview_score)
                # print(app)
                """
                app is a namedtuple(think of it like a immutable dict), with shown attributes, 
                to access an attribute of app, use: app.attribute_name, i.e. app.job_info
                """
                job_apps.append(app)
                # print(cand_profile)

        def sort_key(x):
            try:
                res_score = int(x.app_dict['resume_score'])
            except (ValueError, TypeError):
                res_score = 0

            if x.video_interview_score is None:
                return res_score//2

            elif not x.video_interview_score:
                return res_score//2

            else:
                return (res_score + x.video_interview_score)//2

        job_apps.sort(key=sort_key, reverse=True)
        unique_jobs = [(job.job_info['id'], job.job_info['post']) for job in job_apps]
        unique_jobs = list(set(unique_jobs))

        unique_jobs = [{'id': job[0], 'post': job[1]} for job in unique_jobs]
        # print(job_apps)
        smessage = """
            Congratulations! You are selected as the top performer for the position of {} to receive an offer to join Apli.ai.
            We all are looking forward to working with you and are
            certain that you are going to be a great fit for the team.
            """
        ssubject = 'Hooray! You have been selected for the job'

        rmessage = """
            Thank you for your interest in the position of {} at Apli.ai.We received many promising applications and regret to inform you that we have decided to proceed with other candidates
            and will not take your application further.
            We wish you all the best in your job search and all the other future professional endeavours.
            """
        rsubject = 'Sorry, Please Try again later.'

        return render(request, 'recruiter/candidates.html',
                        {'job_apps': job_apps, 'counts': counts, 'smessage': smessage,
                        'ssubject': ssubject, 'rmessage': rmessage, 'rsubject': rsubject,
                        'account_type': account_type,
                        'notifications': notifications,
                        'interviewers': interviewers,
                        'role': request.session['role'],
                        'unique_jobs': unique_jobs,'company_name':request.session['cname'],
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

    elif request.method == 'POST':

        def get_(x):
            ans = request.POST.get(x, None)
            if isinstance(ans, str):
                return ans.strip()
            return ans

        job_id = get_('job_id')
        cand_id = get_('cand_email')
        cand_name = get_('cand_name')
        job_dict = web_db.collection('jobs').document(job_id).get().to_dict()
        print(job_id, cand_id)
        rec_email = job_dict['email']

        if web_db.collection('applications').document(job_id).collection(
                'applicants').document(cand_id).get().exists:
            messages.error(request, 'This candidate has already applied for this job')
            return redirect('/recruiter/candidates')

        app_dict = {'candidate_name': cand_name,
                    'grades': None,
                    'resume_score': None,
                    'skills_score': None,
                    'status': 'INVITED',
                    'video_interview_links': None,
                    'videos_resume_score': None,
                    }

        web_db.collection('applications').document(job_id).collection(
            'applicants').document(cand_id).set(app_dict)

        recruiter = web_db.collection('users').document(rec_email).get().to_dict()
        cname = recruiter['company_name']
        # print(reverse('job_detail', kwargs={'jid': get_('job_id')}))

        message = render_to_string('recruiter/add_candidate.html',
                                   {'name': get_('cand_name'),
                                    'post': job_dict['post'],
                                    'cname': cname,
                                    'rec_name': recruiter['name'],
                                    'link_target': 'https://apli-ai.herokuapp.com' + reverse('job_detail',
                                                                                             kwargs={'jid': job_id})}
                                   )
        email_recruiter = EmailMessage(subject='Job invitation from Apli.ai',
                                       body=message,
                                       from_email=settings.EMAIL_HOST_USER,
                                       to=[get_('cand_email')]
                                       )
        email_recruiter.content_subtype = 'html'
        email_recruiter.send()

        if not web_db.collection('links').document(job_id).get().exists:
            dict_ = {
                u'anonymous': 0,
                'career_site': 0,
                'referral': 0,
                'internal_referral': 1,
                u'facebook': 0,
                u'linkedin': 0,
                u'job_id': job_id,
                u'type': 'job',
                u'parent': rec_email
            }
            web_db.collection(u'links').document(job_id).set(dict_)

        else:
            count = web_db.collection('links').document(job_id).get().to_dict()['internal_referral']
            web_db.collection(u'links').document(job_id).update({
                'internal_referral': int(count) + 1,
            })

        return redirect('/recruiter/candidates')


def view_interview(request, jid, candidate_id):
    try:

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

        if 'video_interview_grades' not in application_dict.keys():
            grades = dict()
            for ques in que:
                grades[ques['id']] = None

            web_db.collection('applications').document(jid).collection(
                'applicants').document(candidate_id).update({'video_interview_grades': grades})
            application_dict['video_interview_grades'] = grades

        if 'video_interview_comments' not in application_dict.keys():
            comments = dict()
            for ques in que:
                comments[ques['id']] = None

            web_db.collection('applications').document(jid).collection(
                'applicants').document(candidate_id).update({'video_interview_comments': comments})
            application_dict['video_interview_comments'] = comments

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
            question_dict['grade'] = application_dict['video_interview_grades'].get(ques['id'], None)

            if question_dict['grade'] is None:
                question_dict['grade'] = 0

            question_dict['comment'] = application_dict['video_interview_comments'].get(ques['id'], None)
            questions.append(question_dict)

        questions_length = len(questions)

        # 'ocean' radar data
        job_info = web_db.collection('jobs').document(jid).get().to_dict()
        job_info['id'] = jid

        cand_profile = web_db.collection('candidates').document(candidate_id).get().to_dict()

        app_info = web_db.collection('applications').document(jid).collection('applicants').document(
            candidate_id).get().to_dict()

        appid = candidate_id + jid
        application = collections.namedtuple('application', ['job_info',
                                                             'cand_profile',
                                                             'app_dict',
                                                             'appid',
                                                             'skills_score'])
        skills_score = app_info['skills_score']
        # print(skills_score)
        app = application(job_info=job_info, cand_profile=cand_profile, app_dict=app_info,
                          appid=appid.replace('@', '').replace('.', ''), skills_score=skills_score)

        # job_apps = [app]
        # print(job_apps[0].skills_score)
        return render(request, 'recruiter/viewinterview.html',
                        {'application_dict': application_dict, 'questions': questions,
                        'questions_length': questions_length, 'role': 'video-interview',
                        'name': request.session['name'],
                        'company_name': request.session['cname'],
                        'notifications': notifications,
                         'job_app': app,
                        })

    except Exception as e:
        print(e)
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