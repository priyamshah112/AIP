from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.views import View
from firebase_admin import firestore
from collections import namedtuple

db = firestore.client()

"""
A candidate has the following fields:
-Name
-E-mail
-Phone number
-Profile picture
-Date of birth
-Gender
-Address
-Education ( can have multiple entries )
  -degree/education field
    - institute
    - branch/specialisation
    - CGPA/score
    - passYear
-Experience ( can have multiple entries )
  -designation/experience field
    - company
    - duration
    - extra info
    - experience type
-skills
-achievements
-profile_status: True (complete) or False (pending)

-video resume link

-psycology score
  - a : score
  - b : score
    .
    .
    .
- application array ( applied jobs )
"""


def profile(request):
    if request.method == 'GET':
        candidate_id = request.session.get('email')
        candidate_ref = db.collection('candidates').document(candidate_id).get()
        profile_status = candidate_ref.get('profile_status')
        if profile_status == 'empty':
            messages.error(request, 'please complete your basic details')
            return render(request, 'candidate/resume_profile_buildup.html', {'profile_status': profile_status})

        context = {
            'candidate': candidate_ref.to_dict()
        }

        # patch
        if context['candidate']['psycho_ques'] is not None:
            all_ques = db.collection('candPsychoQues').document('all_ques').get().to_dict()
            all_ques = sorted(all_ques.items(), key=lambda x: x[0])

            context['candidate']['psycho_ques'] = sorted(context['candidate']['psycho_ques'].items(),
                                                         key=lambda x: x[0]
                                                         )
            for i in range(0, len(context['candidate']['psycho_ques'])):
                context['candidate']['psycho_ques'][i] = (context['candidate']['psycho_ques'][i][0],
                                                          all_ques[i][1],
                                                          context['candidate']['psycho_ques'][i][1])
        # print(context)
        return render(request, 'candidate/profile.html', context)

    elif request.method == 'POST':
        """
        This is the request structure:
        >>> {
            'name': ['Manthan Chauhan'], 'email': ['manthanchauhan931@gmail.com'],
            'ph_no': ['7042756268'], 'dob': ['1998-11-13'], 'address': ['secret'],
            'profilePicture': [''], 'skills[]': ['HTML'],

            'degree[]': ['B Tech', ''], 'institute[]': ['MAIT', ''], 'branch[]': ['ECE', ''],
            'score[]': ['8.2', ''], 'passingYear[]': ['2020', ''],

            'designation[]': ['Django Developer', ''], 'company[]': ['apli.ai', ''],
            'from[]': ['2019-07', ''], 'to[]': ['2019-08', ''],
            'info[]': ['Backend developer', ''],

            'proName[]': ['Newspapers', ''], 'proDis[]': ['newspaper bill management app', ''],
            'proDate[]': ['2019-04', '']

            'awardDis[]': ['4* rating on codechef', ''], 'awardDate[]': ['2019-07', '']
            }
        """
        # we can remove this one dev is complete
        print(request.POST)

        def get_(x):
            return request.POST.get(x).strip()

        candidate_dict = {
            'name': get_('name'),
            'email': request.session['email'],
            'ph_no': get_('ph_no'),
            'dob': get_('dob'),
            'gender': request.POST.get('gender'),
            'address': get_('address'),
            'profile_picture': request.POST.get('profile_picture'),
            'education': [],    # to be filled
            'experience': [],   # to be filled
            'projects': [],     # to be filled
            'video_resume': None,
            'skills': request.POST.getlist('skills[]'),
            'profile_status': 'partial',
            'psycho_ques': None,
            'award': []     # to be filled
        }

        def null_filter(x):
            for data in x:
                if not data:
                    return False
            return True

        awards = list(zip(request.POST.getlist('awardDis[]'), request.POST.getlist('awardDate[]')
                          ))
        awards = list(filter(null_filter, awards))

        # (degree, institute, branch, score, passYear)
        education_det = list(zip(request.POST.getlist('degree[]'), request.POST.getlist('institute[]'),
                                 request.POST.getlist('branch[]'), request.POST.getlist('score[]'),
                                 request.POST.getlist('passingYear[]')
                                 ))
        education_det = list(filter(null_filter, education_det))

        # (info1, info2, info3)
        info = list(zip(request.POST.getlist('info1[]'), request.POST.getlist('info2[]'),
                        request.POST.getlist('info3[]')
                        ))

        def shorten_info(x):
            ans = []
            for info_ in x:
                if info_:
                    ans.append(info_)
                else:
                    return ans
            return ans

        info = [shorten_info(info_) for info_ in info]
        # print(info)

        # (company, designation, from, to, info, type)
        training_det = list(zip(request.POST.getlist('company[]'), request.POST.getlist('designation[]'),
                                request.POST.getlist('from[]'), request.POST.getlist('to[]'),
                                info, request.POST.getlist('expType[]')))
        # print(training_det)
        training_det = list(filter(null_filter, training_det))

        # (name, info, date)
        project_det = list(zip(request.POST.getlist('proName[]'), request.POST.getlist('proDis[]'),
                               request.POST.getlist('proDate[]')))
        project_det = list(filter(null_filter, project_det))

        for degree, institute, branch, score, passYear in education_det:
            course = {'score': float(score), 'specialisation': branch.strip(),
                      'education': degree.strip(), 'institute': institute.strip(),
                      'passYear': int(passYear)}
            candidate_dict['education'].append(course)

        for company, designation, from_, to, info, expType in training_det:
            internship = {'company': company.strip(), 'designation': designation.strip(),
                          'from': from_, 'to': to, 'info': info, 'type': expType}
            candidate_dict['experience'].append(internship)

        for name, info, date in project_det:
            project = {'name': name.strip(), 'info': info.strip(), 'date': date.strip()}
            candidate_dict['projects'].append(project)

        for info, date in awards:
            award = {'description': info, 'date': date}
            candidate_dict['award'].append(award)

        db.collection('candidates').document(candidate_dict['email']).set(candidate_dict)
        messages.success(request, 'your profile has been updated')
        return JsonResponse({'success': 'True'})



def jobsboard(request):
    # getting the generator for the jobs whose status is opened.
    job_docs = db.collection(u'jobs').where(u'status',u'==',u'Opened').get()
    # company_jobs is the list of job_id's whose status is defined as opened.
    company_jobs = []
    # counting the number of jobs by 'post' and storing it in jobs_count
    jobs_opnd = {}
    jobs_count = {}
    for job in job_docs:
        # appeding the details of the job to the jobs_opnd list.
        # jobs_opnd.append(job.to_dict())
        # print(job.to_dict()['email'])
        jobs_opnd[job.id.strip()]=job.to_dict()
        jobs_opnd[job.id.strip()]["cmpnm"] = db.collection(u'users').document(job.to_dict()['email']).get().to_dict()['company_name']
        #appending the job-id's to the company_jobs array.
        # the logic for counting the number of jobs postwise.
        company_jobs.append(job.id.strip())
        if not str(job.to_dict()['post']) in jobs_count:
            jobs_count[str(job.to_dict()['post'])] = 1
        else:
            jobs_count[str(job.to_dict()['post'])] += 1
    # comment out the lines in case you want to see the data by yourself.
    # print("printing jobs")
    # print("count: ")
    # print(jobs_count)
    # print("job_id's:")
    # print(company_jobs)
    # print(jobs_opnd)
    return render(request, 'candidate/jobs.html',{'jobsss':jobs_opnd})



def resume(request):
    if request.method == 'GET':
        candidate_id = request.session.get('email')
        candidate_ref = db.collection('candidates').document(candidate_id).get()

        if candidate_ref.get('profile_status') == 'empty':
            messages.error(request, 'please complete your basic details')
            return render(request, 'candidate/resume_profile_buildup.html')

        return render(request, 'candidate/resume.html',
                      {'candidate': candidate_ref.to_dict()}
                      )

    if request.method == 'POST':
        print(request.POST)

        def get_(x, y=None):
            ans = request.POST.get(x, y)
            if ans == '':
                ans = y
            if isinstance(ans, str):
                return ans.strip()
            return ans

        def null_filter(x):
            for data in x:
                if not data:
                    return False
            return True

        edit_type = request.POST.get('edit_type')
        update_data = dict()

        if edit_type == 'basic_info':
            fields_2_update = []
            for key, value in request.POST.items():
                if key != 'edit_type' and value != '':
                    fields_2_update.append(key)

            for key in fields_2_update:
                update_data[key] = get_(key)
            print(update_data,"pri")

        elif edit_type == 'skills':
            # removing this if will cause data loss in skills
            if 'skills[]' not in request.POST.keys():
                return JsonResponse({'success': 'True'})

            update_data['skills'] = request.POST.getlist('skills[]')

        elif edit_type == 'del_edu':
            del_edu = get_('education')
            candidate_ref = db.collection('candidates').document(request.session['email']).get().to_dict()
            education = list(filter(lambda x: True if x['education'] != del_edu else False,
                                    candidate_ref['education'])
                             )
            update_data['education'] = education

        elif edit_type == 'add_edu':
            education_det = list(zip(request.POST.getlist('degree[]')[::-1], request.POST.getlist('institute[]')[::-1],
                                     request.POST.getlist('branch[]')[::-1], request.POST.getlist('score[]')[::-1],
                                     request.POST.getlist('passingYear[]')[::-1]
                                     )
                                 )

            education_det = list(filter(null_filter, education_det))
            candidate_ref = db.collection('candidates').document(request.session['email']).get().to_dict()
            exist_education = [x['education'] for x in candidate_ref['education']]

            for degree, institute, branch, score, passYear in education_det:
                if degree not in exist_education:
                    course = {'score': float(score), 'specialisation': branch.strip(),
                              'education': degree.strip(), 'institute': institute.strip(),
                              'passYear': int(passYear)}
                    candidate_ref['education'].append(course)

            update_data['education'] = candidate_ref['education']

        elif edit_type == 'add_exp':
            def shorten_info(x):
                ans = []
                for info_ in x:
                    if info_:
                        ans.append(info_)
                    else:
                        return ans
                return ans

            info = list(zip(request.POST.getlist('info1[]'),
                            request.POST.getlist('info2[]'),
                            request.POST.getlist('info3[]')
                            ))

            info = [shorten_info(info_) for info_ in info]

            training_det = list(zip(request.POST.getlist('company[]')[::-1],
                                    request.POST.getlist('designation[]')[::-1],
                                    request.POST.getlist('from[]')[::-1],
                                    request.POST.getlist('to[]')[::-1], info[::-1],
                                    request.POST.getlist('expType[]')[::-1]
                                    )
                                )
            # print(training_det)

            training_det = list(filter(null_filter, training_det))
            candidate_ref = db.collection('candidates').document(request.session['email']).get().to_dict()
            exist_exp = [(x['company'], x['designation']) for x in candidate_ref['experience']]

            for company, designation, from_, to, info, type in training_det:
                if (company, designation) not in exist_exp:
                    internship = {'company': company.strip(), 'designation': designation.strip(),
                                  'from': from_, 'to': to, 'info': info, 'type': type}
                    candidate_ref['experience'].append(internship)

            update_data['experience'] = candidate_ref['experience']

        elif edit_type == 'add_proj':
            # (name, info, date)
            project_det = list(zip(request.POST.getlist('proName[]')[::-1], request.POST.getlist('proDis[]')[:-1],
                                   request.POST.getlist('proDate[]')[::-1]))

            project_det = list(filter(null_filter, project_det))
            candidate_ref = db.collection('candidates').document(request.session['email']).get().to_dict()
            exist_proj = [x['name'] for x in candidate_ref['projects']]

            for name, info, date in project_det:
                if name not in exist_proj:
                    project = {'name': name.strip(), 'info': info.strip(), 'date': date.strip()}
                    candidate_ref['projects'].append(project)

            update_data['projects'] = candidate_ref['projects']

        elif edit_type == 'update_edu':
            candidate_ref = db.collection('candidates').document(request.session['email']).get().to_dict()

            for education in candidate_ref['education']:
                if education['education'] == get_('init_edu'):
                    for field in education.keys():
                        education[field] = get_(field, education[field])
                    break

            update_data['education'] = candidate_ref['education']

        elif edit_type == 'del_exp':
            company = get_('company')
            designation = get_('designation')

            candidate_ref = db.collection('candidates').document(request.session['email']).get().to_dict()
            experience = list(filter(lambda x: False if x['company'] == company and x['designation'] == designation else True,
                                     candidate_ref['experience']))
            update_data['experience'] = experience

        elif edit_type == 'update_proj':
            candidate_ref = db.collection('candidates').document(request.session['email']).get().to_dict()

            for project in candidate_ref['projects']:
                if project['name'] == get_('proNameInit'):
                    for field in project.keys():
                        project[field] = get_(field, project[field])
                    break

            update_data['projects'] = candidate_ref['projects']

        elif edit_type == 'del_pro':
            candidate_ref = db.collection('candidates').document(request.session['email']).get().to_dict()

            projects = list(filter(lambda x: True if x['name'] != get_('proName') else False,
                                   candidate_ref['projects']))
            update_data['projects'] = projects

        elif edit_type == 'update_exp':
            candidate_ref = db.collection('candidates').document(request.session['email']).get().to_dict()
            init_com = get_('initialCom')
            init_desig = get_('initialDesig')

            info = []
            for field in request.POST.keys():
                if field[0:4] == 'info':
                    if get_(field) is not None:
                        info.append(get_(field))

            for exp in candidate_ref['experience']:
                if exp['company'] == init_com and exp['designation'] == init_desig:
                    for field in exp:
                        if field == 'info':
                            if info:
                                exp[field] = info
                            continue
                        exp[field] = get_(field, exp[field])
                    break

            update_data['experience'] = candidate_ref['experience']

        elif edit_type == 'add_award':
            awards = list(zip(request.POST.getlist('awardDis[]'), request.POST.getlist('awardDate[]')))
            awards = list(filter(null_filter, awards))
            awards = set(awards)

            candidate_ref = db.collection('candidates').document(request.session['email']).get().to_dict()
            exist_awards = set([(award['description'], award['date'])
                                for award in candidate_ref['award']])
            awards -= exist_awards

            for info, date in awards:
                award = {'description': info, 'date': date}
                candidate_ref['award'].append(award)

            update_data['award'] = candidate_ref['award']

        elif edit_type == 'update_award':
            candidate_ref = db.collection('candidates').document(request.session['email']).get().to_dict()
            exist_awards = candidate_ref['award']
            des_init = get_('des_init')
            date_init = get_('dateaward')

            for award in exist_awards:
                desc, date = award['description'], award['date']
                if desc == des_init and date == date_init:
                    award['description'] = get_('des', award['description'])
                    award['date'] = get_('info', award['date'])

            update_data['award'] = exist_awards

        elif edit_type == 'del_award':
            candidate_ref = db.collection('candidates').document(request.session['email']).get().to_dict()
            exist_awards = candidate_ref['award']
            des_init = get_('award')
            date_init = get_('dateaward')

            for i, award in enumerate(exist_awards):
                desc, date = award['description'], award['date']
                if desc == des_init and date == date_init:
                    exist_awards.pop(i)
                    break

            update_data['award'] = exist_awards

        db.collection('candidates').document(request.session['email']).update(update_data)
        messages.success(request, 'your profile has been updated')
        return JsonResponse({'success': 'True'})



def applications(request):
    email = request.session.get('email')

    """
    logic for getting the job details
    first find out all the jobs and their job-ids
    email remains hardcoded for now but will be dynamic using sessions
    """
    docs = db.collection(u'applications').get()
    comp_apps = {}
    pend_apps = {}

    for job_doc in docs:
        if job_doc.reference.collection('applicants').document(email).get().exists:
            req = db.collection('jobs').document(job_doc.id).get().to_dict()
            # print(req)
            status = job_doc.reference.collection('applicants').document(email).get().to_dict()['status']
            req['status'] = status

            if status == 'PENDING':
                pend_apps[job_doc.id] = req
            else:
                comp_apps[job_doc.id] = req

    return render(request, 'candidate/applications.html', {'comp_apps': comp_apps,
                                                           'pend_apps': pend_apps}
                  )



def jobInterview(request):
    if request.method == 'POST':
        jobId = request.POST.get('job')
        candidate = request.session.get('email')
        if not db.collection(u'applications').document(jobId).collection(u'applicants').document(candidate).get().exists:
            job_doc = db.collection(u'jobs').document(jobId).get().to_dict()
            questions = db.collection(u'users').document(job_doc['email']).collection(u'packages').document(job_doc['packageId']).collection(u'questions').get()
            que = []
            for q in questions:
                que.append(q.to_dict())

            db.collection(u'applications').document(jobId).set({})
            db.collection(u'applications').document(jobId).collection(u'applicants').document(candidate).set({
                'candidate_name': request.session.get('name'),
                'status': "PENDING",
                'video_interview_links': {},
                'resume_score': "7",
                'video_resume_score': "6",
                'skills_score': {'a': 4, 'c': 3, 'e': 5, 'n': 5, 'o': 3},
                'grades': {'1': 3, '2': 6, '3': 6, '4': 5},
            })

            return render(request, 'candidate/job_interview.html', {'jobId': jobId, 'job': job_doc, 'questions': que, 'startFrom': 0})
        else:
            ap = db.collection(u'applications').document(jobId).collection(u'applicants').document(candidate).get()
            apdic = ap.to_dict()
            if apdic['status'] == 'PENDING':
                job_doc = db.collection(u'jobs').document(jobId).get().to_dict()
                questions = db.collection(u'users').document(job_doc['email']).collection(u'packages').document(job_doc['packageId']).collection(u'questions').get()
                que = []
                for q in questions:
                    que.append(q.to_dict())
                d = {k:v for k,v in apdic['video_interview_links'].items() if v != ""}
                startFrom = len(d)
                messages.success(request, 'Continue the mock interview')
                # print("lmao bruh")
                return render(request, 'candidate/job_interview.html', {'jobId': jobId, 'job': job_doc, 'questions': que, 'startFrom': startFrom})
            if apdic['status'] == 'APPLIED':
                messages.success(request, 'Your Application will be soon reviewed.')
                # print("yeee haw")
                return HttpResponseRedirect('applications')
    else:
        return HttpResponseRedirect('jobsboard')


def addApplication(request):
    type = request.POST.get('type')
    if type == 'final':
        candidate = request.session.get('email')
        job = request.POST.get('job')
        db.collection(u'applications').document(job).collection(u'applicants').document(candidate).update({
            'status': "APPLIED"
        })
        messages.success(request, 'Application added successfully.')
        job_doc = db.collection('jobs').document(request.POST.get('job')).get().to_dict()

        return JsonResponse({"success": "True"})
    if type == 'addVideo':
        candidate = request.session.get('email')
        job = request.POST.get('job')
        ids = request.POST.get('ids')
        video_link = request.POST.get('video_link')
        doc_ref = db.collection(u'applications').document(job).collection(u'applicants').document(candidate)
        vd_dic = doc_ref.get().to_dict()['video_interview_links']
        vd_dic.update({ids: video_link})
        doc_ref.update({
            'video_interview_links': vd_dic
        })

        messages.success(request, 'Application added successfully.')
        return JsonResponse({"success": "True"})

