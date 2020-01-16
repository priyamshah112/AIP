from collections import namedtuple
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from firebase_admin import firestore
from django.conf import settings
#from accounts.views import signup
from datetime import datetime
from . import jsonParser, isme
import copy

# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

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


class NotAvailable(Exception):
    pass


def remove_saved_job_relation(job_id,cand_id):
    saved_job   =   list(db.collection('rel_candidate_savedjob').where(u'job_id','==',job_id).where(u'cand_id','==',cand_id).get())
    if not saved_job:
        pass
    else:
        saved_job=saved_job[0]
        saved_job.reference.delete()



def profile(request):
    if request.method == 'GET':
        try:
            candidate_id = request.session.get('email')
            candidate_ref = db.collection('candidates').document(candidate_id).get()
            profile_status = candidate_ref.get('profile_status')
            if profile_status == 'empty':
                messages.error(request, 'please complete your basic details')


                return render(request, 'candidate/resume_profile_buildup.html', {'profile_status': profile_status})

            candidate_dict = candidate_ref.to_dict()
            candidate_dict['dob'] = candidate_dict['dob'].strftime('%B %d, %Y')
            for education in candidate_dict['education']:
                if education['is_current']:
                    pass
                else:
                    education['end'] = education['end'].strftime('%B %Y')
           # skills = candidate_dict['skills'].items()
           # candidate_dict['skills'] = []

           # for name, prof in skills:
           #     candidate_dict['skills'].append(
           #         {'name': name, 'prof': prof}
           #     )

            for training in candidate_dict['experience']:
                training['from'] = training['from'].strftime('%b %Y')
                training['to'] = training['to'].strftime('%b %Y')
            
            for project in candidate_dict['projects']:
                project['from'] = project['from'].strftime('%B %Y')
                project['to'] = project['to'].strftime('%B %Y')


            for award in candidate_dict['award']:
                award['date'] = award['date'].strftime('%B %Y')
            

            return render(request, 'candidate/profile.html')
            
        except (KeyError, AttributeError):
            raise
            # db.collection(u'candidates').document(request.session['email']).update({'profile_status': 'empty'})
            # raise

    elif request.method == 'POST':
        """
        This is the request structure:
        {
            'profile_picture': profilePicURL,
                'ph_no': ph_no_arr,
                'roll_no': rollno_arr,
                'highest_qualification': high_arr,
                
                'first_name': fname_arr,
                'middle_name': mname_arr,
                'last_name': lname_arr,
                'dob': dob_arr,
                'gender': cgender_arr,
                'lang': lang_arr,
                'lang_pro': langp_arr,
                'address': address_arr,
                'city': city_arr,
                'postal_code': pcode_arr,
                'state': state_arr,
                'country': country_arr,

                'sem_score': score_arr,
                'sem_closed_backlog': closedbl_arr,
                'sem_live_backlogs': livebl_arr,
                'average_sem_score': average_arr,
                'total_live_backlogs': tlivebl_arr,
                'total_closed_backlogs': tclosedbl_arr,
                'sem_certi': semcerti_arr,
                
                'XII_School': XIIschool_arr,
                'XII_Stream' : XIIboard_arr,
                'XII_Board': XIIinstitute_arr,
                'XII_Score': XIIscore_arr,
                'XII_Score_Unit': XIIscoreUnit_arr,
                'XII_From': XIIDateFrom_arr,
                'XII_To': XIIDateTo_arr,
                'XII_Certi': XIIcerti_arr,

                'Diploma_School': DiploInst_arr,
                'Diploma_Stream': DiploStream_arr,
                'Diploma_Board': DiploBoard_arr,
                'Diploma_Score': Diploscore_arr,
                'Diploma_Score_unit': DiploscoreUnit_arr,
                'Diploma_From': diploDateFrom_arr,
                'Diploma_To': diploDateTo_arr,
                'Diploma_Certi':diplocerti_arr,

                'X_School': Xinstitute_arr,
                'X_Board': XBoard_arr,
                'X_Score': Xscore_arr,
                'X_Score_Unit': Xscoreunit_arr,
                'X_From': XDateFrom_arr,
                'X_To': XDateTo_arr,
                'X_Certi':Xcerti_arr,

                'Other_Institute': otherinstitute_arr,
                'Other_Board': otherboard_arr,
                'Other_From': otherfrom_arr,
                'Other_To': otherto_arr,
                'Other_Grade': othergrade_arr,
                'Other_Grade_Unit': othergrade_of_arr,
                'Other_Qualification': otherqualification_arr,
                'Other_Branch': otherbranch_arr,
                'Other_Certi': othercerti_arr,

                'Exp_Type': exptype_arr,
                'Exp_Company': expcompany_arr,
                'Exp_from': expfrom_arr,
                'Exp_to': expto_arr,
                'Exp_desig': expdesig_arr,
                'Exp_info1': expinfo1_arr,
                'Exp_info2': expinfo2_arr,
                'Exp_info3': expinfo3_arr,
                'Exp_industry_type': expindtype_arr,
                'Exp_domain': expdomain_arr,
                'Exp_Certi' : expcerti_arr,

                'Project_Name': proName_arr,
                'Project_Uni_or_Company': proUni_arr,
                'Project_from': proFrom_arr,
                'Project_to': proTo_arr,
                'Project_info1': proinfo1_arr,
                'Project_info2': proinfo2_arr,
                'Project_certi': procerti_arr,

                'Leadership_Title': leadTitle_arr,
                'Leadership_organization': commitee_arr,
                'Leadership_from': leadFrom_arr,
                'Leadership_to': leadTo_arr,
                'Leadership_info1': leadinfo1_arr,
                'Leadership_info2': leadinfo2_arr,
                'Leadership_certi': leadcerti_arr,

                'Award_discription': awardDis_arr,
                'Award_date': awardDate_arr,
                
                'data' : skill_ajax,
                'count' : skcount,
                
                'total_certi':certicount
        }
        """
        # we can remove this one dev is complete
        # print(request.POST)
        # return

        def get_(x, alt=None, error=False):
            """
            get key x from request, else return alt if x is absent
            :param x: key to look, string
            :param alt: value to return if x is not a key or x is ''(null)
            :param error: bool, whether to raise error if result is NONE
            :return:
            """
            # find result, else set result as None
            result = request.POST.get(x, alt)
            if result == '':
                result = alt

            # if result is str, remove spaces
            if isinstance(result, str):
                return result.strip()

            # if result is None, raise error if asked
            if error and result is None:
                raise NotAvailable
            return result

        # basic candidate info
        profile_picture = get_('profile_picture', settings.DEFAULT_CAND_PICTURE)

        ph_no = int(list(filter(None, request.POST.getlist('ph_no[]')))[0])
        if ph_no is None:
            messages.error(request, 'please provide phone no & try again')
            return JsonResponse({'success': 'true'})

        highest_qualification = list(filter(None,request.POST.getlist('highest_qualification[]')))[0]
        if highest_qualification is None:
            messages.error(request, 'please provide highest qualification & try again')
            return JsonResponse({'success': 'true'})
     
        roll_no = list(filter(None,request.POST.getlist('roll_no[]')))[0]
        if roll_no is None:
            messages.error(request, 'please provide roll no & try again')
            return JsonResponse({'success': 'true'})
        
        first_name = list(filter(None,request.POST.getlist('first_name[]')))[0]
        if first_name is None:
            messages.error(request, 'please provide name & try again')
            return JsonResponse({'success': 'true'})
        
        middle_name = list(filter(None,request.POST.getlist('middle_name[]')))[0]

        last_name = list(filter(None,request.POST.getlist('last_name[]')))[0]
        if last_name is None:
            messages.error(request, 'please provide name & try again')
            return JsonResponse({'success': 'true'})
        
        email = request.session.get('email', None)
        if email is None:
            messages.error(request, 'Please try again later')
            return JsonResponse({'success': 'true'})
        
        dob = list(filter(None,request.POST.getlist('dob[]')))[0]
        if dob is not None:
            dob = datetime.strptime(dob, '%Y-%m-%d')
        
        gender = list(filter(None,request.POST.getlist('gender[]')))[0]
        if gender is None:
            messages.error(request, 'please provide gender & try again')
            return JsonResponse({'success': 'true'})
           
        address = list(filter(None,request.POST.getlist('address[]')))[0]
        if address is None:
            messages.error(request, 'please provide address & try again')
            return JsonResponse({'success': 'true'})
        
        city = list(filter(None,request.POST.getlist('city[]')))[0]
        if city is None:
            messages.error(request, 'please provide city & try again')
            return JsonResponse({'success': 'true'})

        postal_code = int(list(filter(None,request.POST.getlist('postal_code[]')))[0])
        if postal_code is None:
            messages.error(request, 'please provide postal code & try again')
            return JsonResponse({'success': 'true'})

        state = list(filter(None,request.POST.getlist('state[]')))[0]
        if state is None:
            messages.error(request, 'please provide state & try again')
            return JsonResponse({'success': 'true'})
       
        country = list(filter(None,request.POST.getlist('country[]')))[0]
        if country is None:
            messages.error(request, 'please provide country & try again')
            return JsonResponse({'success': 'true'})
        
        total_certi = int(request.POST.get('total_certi'))

        XII = None
        if len(list(filter(None,request.POST.getlist('XII_School[]')))) > 0:
            try:
                XII = {
                    'education': 'XII',
                    'board': list(filter(None,request.POST.getlist('XII_Board[]')))[0],
                    'certificate': list(filter(None,request.POST.getlist('XII_Certi[]')))[0],
                    'end': datetime.strptime(list(filter(None,request.POST.getlist('XII_To[]')))[0], '%Y-%m'),
                    'institute': list(filter(None,request.POST.getlist('XII_School[]')))[0],
                    'score': float(list(filter(None,request.POST.getlist('XII_Score[]')))[0]),
                    'score_unit': list(filter(None,request.POST.getlist('XII_Score_Unit[]')))[0],
                    'specialization': list(filter(None,request.POST.getlist('XII_Stream[]')))[0],
                    'start': datetime.strptime(list(filter(None,request.POST.getlist('XII_From[]')))[0], '%Y-%m'),
                    'is_current': False,
                }
               
            except NotAvailable:
                messages.error(request, 'Insufficient information for XII')
                XII = None
        else :
            XII = {
                    'education': 'XII',
                    'institute': '',
                    'specialization': '',
                    'score': '',
                    'score_unit': '',
                    'board': '',
                    'start' : datetime.strptime('0001-01', '%Y-%m'),
                    'end' : datetime.strptime('0001-01', '%Y-%m'),
                    'certificate': 'Certificate not uploaded' ,
                    'is_current': False,
                }
      
        diploma = None
        if len(list(filter(None,request.POST.getlist('Diploma_School[]')))) > 0:
            try:
                diploma = {
                    'education': 'Diploma',
                    'board': list(filter(None,request.POST.getlist('Diploma_Board[]')))[0],
                    'certificate': list(filter(None,request.POST.getlist('Diploma_Certi[]')))[0],
                    'end': datetime.strptime(list(filter(None,request.POST.getlist('Diploma_To[]')))[0], '%Y-%m'),
                    'institute': list(filter(None,request.POST.getlist('Diploma_School[]')))[0],
                    'score': float(list(filter(None,request.POST.getlist('Diploma_Score[]')))[0]),
                    'score_unit': list(filter(None,request.POST.getlist('Diploma_Score_unit[]')))[0],
                    'specialization': list(filter(None,request.POST.getlist('Diploma_Stream[]')))[0],
                    'start': datetime.strptime(list(filter(None,request.POST.getlist('Diploma_From[]')))[0], '%Y-%m'),
                    'is_current': False,
                }

            except NotAvailable:
                messages.error(request, 'Insufficient information for Diploma')
                diploma = None
        # else:
        #     diploma = {
        #             'education': 'Diploma',
        #             'institute': '',
        #             'specialization': '',
        #             'board': '',
        #             'score': '',
        #             'score_unit': '',
        #             'start': datetime.strptime('0001-01', '%Y-%m'),
        #             'end': datetime.strptime('0001-01', '%Y-%m'),
        #             'certificate': 'Certificate not uploaded'
        #         }
       
        X = None
        if len(list(filter(None,request.POST.getlist('X_School[]')))) > 0:
            try:
                X = {
                    'education': 'X',
                    'board': list(filter(None,request.POST.getlist('X_Board[]')))[0],
                    'certificate': list(filter(None,request.POST.getlist('X_Certi[]')))[0],
                    'end': datetime.strptime(list(filter(None,request.POST.getlist('X_To[]')))[0], '%Y-%m'),
                    'institute': list(filter(None,request.POST.getlist('X_School[]')))[0],
                    'score': float(list(filter(None,request.POST.getlist('X_Score[]')))[0]),
                    'score_unit': list(filter(None,request.POST.getlist('X_Score_Unit[]')))[0],
                    'start': datetime.strptime(list(filter(None,request.POST.getlist('X_From[]')))[0], '%Y-%m'),
                    'specialization': 'General',
                    'is_current': False,
                }

            except NotAvailable:
                messages.error(request, 'Insufficient information for X')
                X = None
        else:
             X = {
                    'education': 'X',
                    'institute': '',
                    'board': '',
                    'score': '',
                    'score_unit': '',
                    'start': datetime.strptime('0001-01', '%Y-%m'), 
                    'end': datetime.strptime('0001-01', '%Y-%m'),
                    'certificate': 'Certificate not uploaded',
                    'specialization': 'General',
                    'is_current': False,
                }

        
        lang_names = list(filter(None,request.POST.getlist('lang[]')))
        lang_proficiencies = list(filter(None,request.POST.getlist('lang_pro[]'))) 
        items = list(zip(lang_names, lang_proficiencies))
        languages = dict(items)

        #skill_names = list(filter(None,request.POST.getlist('Skill_discription[]'))) 
        #skill_pros = list(filter(None,request.POST.getlist('Skill_proficiency[]'))) 
        #skills = dict(list(zip(skill_names, skill_pros)))


        candidate_dict = {
            'profile_picture': profile_picture,
            'ph_no': ph_no,
            'roll_no': roll_no,
            'highest_qualification': highest_qualification,
            'First_name': first_name,
            'Middle_name': middle_name,
            'Last_name': last_name,
            'email': email,
            'dob': dob,
            'address':address,
            'city':city,
            'postal_code':postal_code,
            'state':state,
            'country':country,
            'gender': gender,
            'languages': languages,
            'education': list(filter(lambda x: True if x is not None else False, [X, XII, diploma])), #current and other to be filled
            'experience': [],  # to be filled 
            'projects': [],  # to be filled 
            'extra_curricular': [],  # to be filled 
            'video_resume': None,
            'skills': [], #to be filled
            'profile_status': 'partial',
            'psycho_ques': None,
            'award': [],  # to be filled
            'total_certicount' : total_certi #number of certificates uploaded by candidate 
        }

       # print("1", candidate_dict)

        def null_filter(x):
            for data in x:
                if not data:
                    return False
            return True
        #Award_discription,Award_date
        awardDis = list(filter(None,request.POST.getlist('Award_discription[]')))
        awardDate = list(filter(None,request.POST.getlist('Award_date[]')))
        awards = list(zip(awardDis,awardDate))
        for info, date in awards:
            award = {'description': info, 'date': datetime.strptime(date, '%Y-%m')}
            candidate_dict['award'].append(award)

        # Other_Institute,Other_Board,Other_From,Other_To,Other_Grade,Other_Grade_Unit,Other_Qualification,Other_Branch,Other_Certi
        Other_Institute = list(filter(None,request.POST.getlist('Other_Institute[]')))
        Other_Board = list(filter(None,request.POST.getlist('Other_Board[]')))
        Other_From = list(filter(None,request.POST.getlist('Other_From[]')))
        Other_To = list(filter(None,request.POST.getlist('Other_To[]')))
        Other_Grade = list(filter(None,request.POST.getlist('Other_Grade[]')))
        Other_Grade_Unit = list(filter(None,request.POST.getlist('Other_Grade_Unit[]')))
        Other_Qualification = list(filter(None,request.POST.getlist('Other_Qualification[]')))
        Other_Branch = list(filter(None,request.POST.getlist('Other_Branch[]')))
        Other_Certi = list(filter(None,request.POST.getlist('Other_Certi[]')))

        education_det = list(zip(Other_Institute,Other_Board,Other_From,Other_To,Other_Grade,Other_Grade_Unit,Other_Qualification,Other_Branch,Other_Certi))

        for institute, board, From , to, grade, grade_unit, quali, branch, certi in education_det:
            course = { 'education' : quali,
                        'institute' : institute,
                        'specialization' : branch,
                        'board' : board,
                        'score' : float(grade),
                        'score_unit' : grade_unit,
                        'start' : datetime.strptime(From, '%Y-%m'),
                        'end' : datetime.strptime(to, '%Y-%m'),
                        'certificate' : certi,
                       'is_current': False,
                    }
            candidate_dict['education'].append(course)

        #sem_score,sem_closed_backlog,sem_live_backlogs,average_sem_score,total_live_backlogs,total_closed_backlogs,sem_certi
        batch = list(db.collection(u'rel_batch_candidates').where(u'candidate_id', u'==', email).stream())[0]
        batch = batch.to_dict().get(u'batch_id')
        batch = db.collection(u'batches').document(batch).get().to_dict()

        college = batch['college']
        college = list(db.collection(u'users').where(u'college', u'==', college).stream())[0].to_dict()

        def score_unit(number):
            if number == 100:
                return '%'
            else:
                return '/' + str(number)

        current_ed = {
            'education': batch['course'],
            'board': college['board'],
            'certificate': None,
            'end': None,
            'institute': batch['college'],
            'score': list(request.POST.getlist('average_sem_score[]'))[0],
            'score_unit': score_unit(batch['grade']),
            'specialization': batch['branch'],
            'start': int(batch['batch_year'][:4]),
            'is_current': True,
            'sem_records': [],
            'total_live_backlogs': int(request.POST.getlist('total_live_backlogs[]')[0]),
            'total_closed_backlogs': int(request.POST.getlist('total_closed_backlogs[]')[0]),
        }

        semesters = []

        sem_score = list(request.POST.getlist('sem_score[]'))
        sem_closed_backlog = list(request.POST.getlist('sem_closed_backlog[]'))
        sem_live_backlogs = list(request.POST.getlist('sem_live_backlogs[]'))
        sem_certi = list(request.POST.getlist('sem_certi[]'))

        sem_det = list(zip(sem_score,sem_closed_backlog,sem_live_backlogs,sem_certi))

        for sem,closed,live,certi in sem_det:
            semester = {
                'semester_score' : sem,
                'closed_backlog' : closed,
                'live_backlog' : live,
                'certificate' : certi
            }

            semesters.append(semester)

        current_ed['sem_records'] = semesters
        candidate_dict['education'].append(current_ed)


        '''
        # (info1, info2, info3)
        info = list(zip(request.POST.getlist('info1[]'), request.POST.getlist('info2[]'),
                        request.POST.getlist('info3[]')
                        ))
        curricular_info = list(zip(request.POST.getlist('lead_1[]'),
                                   request.POST.getlist('lead_2[]')
                                   ))
        '''

        def shorten_info(x):
            ans = []
            for info_ in x:
                if info_:
                    ans.append(info_)
                else:
                    return ans
            return ans
        '''
        info = [shorten_info(info_) for info_ in info]
        curricular_info = [shorten_info(info_) for info_ in curricular_info]
        '''

        # Exp_Type,Exp_Company,Exp_from,Exp_to,Exp_desig,Exp_info1,Exp_info2,Exp_info3,Exp_industry_type,Exp_domain,Exp_Certi
        Exp_Type = list(filter(None,request.POST.getlist('Exp_Type[]')))
        Exp_Company = list(filter(None,request.POST.getlist('Exp_Company[]')))
        Exp_from = list(filter(None,request.POST.getlist('Exp_from[]')))
        Exp_to = list(filter(None,request.POST.getlist('Exp_to[]')))
        Exp_desig = list(filter(None,request.POST.getlist('Exp_desig[]')))
        Exp_info = list(zip(list(filter(None,request.POST.getlist('Exp_info1[]'))),
                            list(filter(None,request.POST.getlist('Exp_info2[]'))),
                            list(filter(None,request.POST.getlist('Exp_info3[]')))))
        Exp_info = [shorten_info(info_) for info_ in Exp_info] #adding info in one line
        Exp_industry_type = list(filter(None,request.POST.getlist('Exp_industry_type[]')))
        Exp_domain = list(filter(None,request.POST.getlist('Exp_domain[]')))
        Exp_Certi = list(filter(None,request.POST.getlist('Exp_Certi[]')))

        training_det = list(zip(Exp_Type,Exp_Company,Exp_from,Exp_to,Exp_desig,Exp_info,Exp_industry_type,Exp_domain,Exp_Certi))
        for Type,comp,From,to,desig,info,indus,domain,certi in training_det:
            course = { 'Type' : Type,
                        'company' : comp,
                        'from' : datetime.strptime(From, '%Y-%m'),
                        'to' : datetime.strptime(to, '%Y-%m'),
                        'designation' : desig,
                        'information' : info,
                        'industry' : indus,
                        'domain' : domain,
                        'certificate' : certi 
                    }
            candidate_dict['experience'].append(course)
        

        # Project_Name,Project_Uni_or_Company,Project_from,Project_to,Project_info1,Project_info2,Project_certi
        Project_Name = list(filter(None,request.POST.getlist('Project_Name[]')))
        Project_Uni_or_Company = list(filter(None,request.POST.getlist('Project_Uni_or_Company[]')))
        Project_from = list(filter(None,request.POST.getlist('Project_from[]')))
        Project_to = list(filter(None,request.POST.getlist('Project_to[]')))
        Project_info = list(zip(list(filter(None,request.POST.getlist('Project_info1[]'))),
                                list(filter(None,request.POST.getlist('Project_info2[]')))))
        Project_info = [shorten_info(info_) for info_ in Project_info] #adding info in one line
        Project_certi = list(filter(None,request.POST.getlist('Project_certi[]')))

        project_det = list(zip(Project_Name,Project_Uni_or_Company,Project_from,Project_to,Project_info,Project_certi))
        for name,uni,From,to,info,certi in project_det:
            course = { 'Name' : name,
                        'University_Company' : uni,
                        'from' : datetime.strptime(From, '%Y-%m'),
                        'to' : datetime.strptime(to, '%Y-%m'),
                        'information' : info,
                        'certificate' : certi
                    }
            candidate_dict['projects'].append(course)

        # Leadership_Title,Leadership_organization,Leadership_from,Leadership_to,Leadership_info1,Leadership_info2,Leadership_certi
        Leadership_Title = list(filter(None,request.POST.getlist('Leadership_Title[]')))
        Leadership_organization = list(filter(None,request.POST.getlist('Leadership_organization[]')))
        Leadership_from = list(filter(None,request.POST.getlist('Leadership_from[]')))
        Leadership_to = list(filter(None,request.POST.getlist('Leadership_to[]')))
        Leadership_info = list(zip(list(filter(None,request.POST.getlist('Leadership_info1[]'))),
                                    list(filter(None,request.POST.getlist('Leadership_info2[]'))) ))    
        Leadership_info = [shorten_info(info_) for info_ in Leadership_info] #adding info in one line
        Leadership_certi = list(filter(None,request.POST.getlist('Leadership_certi[]')))

        curricular_det = list(zip(Leadership_Title,Leadership_organization,Leadership_from,Leadership_to,Leadership_info,Leadership_certi))
        for role, org, From, to, info, certi in curricular_det:
            activity = {'role': role, 
                            'organisation': org,
                            'start': datetime.strptime(From, '%Y-%m'),
                            'end': datetime.strptime(to, '%Y-%m'),
                            'info': info,
                            'certificate' : certi
                            }
            candidate_dict['extra_curricular'].append(activity)
        # return JsonResponse({'success': 'true'})
        
        #data,count  (Skills)
        count = int(list(filter(None,request.POST.get('count')))[0])
        for i in range(0,count-1):
            dadict = []
            var = 'data['+str(i)+'][]'
            data = list(filter(None,request.POST.getlist(var)))
            name = data[0] #name of sub group
            subcount = int(data[1]) #count of skills in that group
            for j in range(0,subcount):
                var1 = 'data['+str(i)+']['+str(j)+'][]'
                sk = list(filter(None,request.POST.getlist(var1)))
                dadict.append({sk[0] : sk[1]})
            candidate_dict['skills'].append({name : dadict})

        #print(candidate_dict)

        # create a deep copy of cand_dict and create a pdfResume
        copy_dict = copy.deepcopy(candidate_dict)
        link = generate_pdf(copy_dict)
        candidate_dict['pdfResume'] = link

        if db.collection(u'candidates').document(candidate_dict['email']).get().exists:
            db.collection('candidates').document(candidate_dict['email']).update(candidate_dict)
        else:
            db.collection('candidates').document(candidate_dict['email']).set(candidate_dict)

        messages.success(request, 'your profile has been updated')
        return JsonResponse({'success': True})
    


def jobsboard(request):
    if request.session.get('hidename', None) is not None:
        return HttpResponseRedirect('/')

    cand_dict = db.collection(u'candidates').document(request.session['email']).get().to_dict()

    if 'freeze' in cand_dict.keys() and cand_dict['freeze']:
        messages.error(request, 'You cannot view any job posts')
        messages.error(request, 'You have been frozen by your training & placement officer')
        # print('here')
        return redirect('/candidate/profile')

    placements = db.collection(u'rel_placement_candidates').where(
        u'candidate_id', u'==', request.session['email']).get()
    placements = [placement.to_dict()['placement_id'] for placement in placements]

    job_ids = list()
    for id_ in placements:
        jobs = db.collection(u'rel_placement_jobs').where(
            u'placement_id', u'==', id_).where(u'status', u'==', u'open').get()
        jobs = [doc.to_dict()['job_id'] for doc in jobs]
        job_ids += jobs

    job_ids = list(set(job_ids))
    # print(job_ids)
    job_docs = [db.collection(u'jobs').document(id_).get() for id_ in job_ids]

    def closed_filter(doc):
        try:
            status = doc.to_dict()['status']
        except KeyError:
            return False
        return status != 'Closed'

    for doc in job_docs:
        if datetime.strptime(doc.to_dict()['deadline'], '%Y-%m-%d') < datetime.now():
            doc.to_dict()['status'] = 'Closed'
            db.collection('jobs').document(doc.reference.id).update({'status': 'Closed'})

    job_docs = list(filter(closed_filter, job_docs))
    company_jobs = []
    # counting the number of jobs by 'post' and storing it in jobs_count
    jobs_opnd = {}
    jobs_count = {}
    for job in job_docs:
        # appeding the details of the job to the jobs_opnd list.
        # jobs_opnd.append(job.to_dict())
        # print(job.to_dict()['email'])
        jobs_opnd[job.id.strip()] = job.to_dict()

        try:
            if 'by_campus' in job.to_dict().keys():
                jobs_opnd[job.id.strip()]['cmpnm'] = db.collection(u'users').document(
                    job.to_dict()['email']).get().to_dict()['college']
            else:
                jobs_opnd[job.id.strip()]["cmpnm"] = db.collection(u'users').document(
                    job.to_dict()['email']).get().to_dict()['company_name']
        except TypeError:
            db.collection(u'jobs').document(job.id).delete()
            db.collection(u'applications').document(job.id).delete()
            rels = db.collection(u'rel_placement_jobs').where(u'job_id', u'==', job.id).get()

            for rel in rels:
                rel.reference.delete()
            continue

        # appending the job-id's to the company_jobs array.
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
    # # print(jobs_opnd)
    # paginator = Paginator(jobs_opnd, 1) # Show 25 contacts per page
    # page = request.GET.get('page', 1)
    # # jobs_opnd = paginator.get_page(page)
    # try:
    #     jobs_opnd = paginator.page(page)
    # except PageNotAnInteger:
    #     jobs_opnd = paginator.page(1)
    # except EmptyPage:
    #     jobs_opnd = paginator.page(paginator.num_pages)

    # jobs from campus placement
    # get placement ids for candidate
    candidate_id = request.session.get('email')
    placement_ids = []
    placement_candidates = db.collection('rel_placement_candidates').where(
        'candidate_id', '==', candidate_id).get()
    for placement_candidate in placement_candidates:
        placement_ids.append(placement_candidate.get('placement_id'))

    # get open jobs for each placement
    job_ids = []
    for placement_id in placement_ids:
        placement_jobs = db.collection('rel_placement_jobs').where(
            'placement_id', '==', placement_id).where('status', '==', 'open').get()
        for placement_job in placement_jobs:
            job_ids.append(placement_job.get('job_id'))

    for job_id in job_ids:
        job = db.collection('jobs').document(job_id).get()
        jobs_opnd[job.id.strip()] = job.to_dict()

        if 'by_campus' in job.to_dict().keys():
            jobs_opnd[job.id.strip()]['cmpnm'] = db.collection(u'users').document(
                job.to_dict()['email']).get().to_dict()['college']
        else:
            jobs_opnd[job.id.strip()]["cmpnm"] = db.collection(u'users').document(
                job.to_dict()['email']).get().to_dict()['company_name']
        # appending the job-id's to the company_jobs array.
        # the logic for counting the number of jobs postwise.
        company_jobs.append(job.id.strip())
        if not str(job.to_dict()['post']) in jobs_count:
            jobs_count[str(job.to_dict()['post'])] = 1
        else:
            jobs_count[str(job.to_dict()['post'])] += 1

    return render(request, 'candidate/jobs.html', {'jobsss': jobs_opnd})



def resume(request):
    if request.method == 'GET':
        candidate_id = request.session.get('email')
        candidate_ref = db.collection('candidates').document(candidate_id).get()

        if candidate_ref.get('profile_status') == 'empty':
            messages.error(request, 'please complete your basic details')
            return render(request, 'candidate/resume_profile_buildup.html')

        from classes import Counter

        # get info about current education
        candidate_dict = candidate_ref.to_dict()
        current_education = None

        # for education in candidate_dict['education']:
        #     if education['is_current']:
        #         current_education = education

        # get batch info
        #batch_id = get_batch(candidate_id)
        #batch = db.collection(u'batches').document(batch_id).get().to_dict()

        #current_education['duration'] = batch['batch_year']
        #current_education['branch'] = batch['branch']
        batch_id=101
        batch = 'B3'
        current_education['duration']='2020'
        current_eductaion['branch']='Computer Engineering'

        return render(request, 'candidate/resume.html',
                      {'candidate': candidate_ref.to_dict(),
                       'counter': Counter(1),
                       'current_education': current_education,
                       }
                      )

    if request.method == 'POST':
        # print(request.POST)

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
        def shorten_info(x):
                ans = []
                for info_ in x:
                    if info_:
                        ans.append(info_)
                    else:
                        return ans
                return ans

        if edit_type == 'basic_info':
            First_name = list(filter(None,request.POST.getlist('First_name[]')))[0]
            Middle_name = list(filter(None,request.POST.getlist('Middle_name[]')))[0]
            Last_name = list(filter(None,request.POST.getlist('Last_name[]')))[0]
            ph_no = int(list(filter(None,request.POST.getlist('ph_no[]')))[0])
            dob = list(filter(None,request.POST.getlist('dob[]')))[0]
            dob = datetime.strptime(dob, '%Y-%m-%d')
            address = list(filter(None,request.POST.getlist('address[]')))[0]
            city = list(filter(None,request.POST.getlist('city[]')))[0]
            postal_code = int(list(filter(None,request.POST.getlist('postal_code[]')))[0])
            state = list(filter(None,request.POST.getlist('state[]')))[0]
            country = list(filter(None,request.POST.getlist('country[]')))[0]
            gender = list(filter(None,request.POST.getlist('gender[]')))[0]
            lang_names = list(filter(None,request.POST.getlist('languages[]')))
            lang_proficiencies = list(filter(None,request.POST.getlist('lang_pro[]'))) 
            items = list(zip(lang_names, lang_proficiencies))
            languages = dict(items)
            profile_picture = list(filter(None,request.POST.getlist('profile_picture[]')))[0]
            update_data = {
                'First_name' : First_name,
                'Middle_name' : Middle_name,
                'Last_name' : Last_name,
                'ph_no' : ph_no,
                'dob' : dob,
                'address' : address,
                'city' : city,
                'postal_code' : postal_code,
                'state' : state,
                'country' : country,
                'gender' : gender,
                'languages' : languages,
                'profile_picture' : profile_picture
            }
        elif edit_type == 'skills':
            # removing this if will cause data loss in skills
            if 'skills[]' not in request.POST.keys():
                return JsonResponse({'success': 'True'})
            update_data = dict()
            update_data['skills'] = request.POST.getlist('skills[]')

        elif edit_type == 'del_edu':
            del_edu = get_('education')
            candidate_ref = db.collection('candidates').document(request.session['email']).get().to_dict()
            education = list(filter(lambda x: True if x['education'] != del_edu else False,
                                    candidate_ref['education'])
                             )
            update_data = dict()
            update_data['education'] = education

        elif edit_type == 'add_edu':
            XII = None
            if len(list(filter(None,request.POST.getlist('XII_School[]')))) > 0:
                try:
                    XII = {
                        'education': 'XII',
                        'institute': list(filter(None,request.POST.getlist('XII_School[]')))[0],
                        'specialization': list(filter(None,request.POST.getlist('XII_Stream[]')))[0],
                        'score': float(list(filter(None,request.POST.getlist('XII_Score[]')))[0]),
                        'score_unit': list(filter(None,request.POST.getlist('XII_Score_Unit[]')))[0],
                        'board': list(filter(None,request.POST.getlist('XII_Board[]')))[0],
                        'start': datetime.strptime(list(filter(None,request.POST.getlist('XII_From[]')))[0], '%Y-%m'),
                        'end': datetime.strptime(list(filter(None,request.POST.getlist('XII_To[]')))[0], '%Y-%m'),
                        'certificate': list(filter(None,request.POST.getlist('XII_Certi[]')))[0],
                        'is_current': False,
                    }
                
                except NotAvailable:
                    messages.error(request, 'Insufficient information for XII')
                    XII = None
            else :
                XII = {
                        'education': 'XII',
                        'institute': '',
                        'specialization': '',
                        'score': '',
                        'score_unit': '',
                        'board': '',
                        'start' : datetime.strptime('0001-01', '%Y-%m'),
                        'end' : datetime.strptime('0001-01', '%Y-%m'),
                        'certificate': 'Certificate not uploaded' ,
                        'is_current': False,
                    }
        
            diploma = None
            if len(list(filter(None,request.POST.getlist('Diploma_School[]')))) > 0:
                try:
                    diploma = {
                        'education': 'Diploma',
                        'institute': list(filter(None,request.POST.getlist('Diploma_School[]')))[0],
                        'specialization': list(filter(None,request.POST.getlist('Diploma_Stream[]')))[0],
                        'board': list(filter(None,request.POST.getlist('Diploma_Board[]')))[0],
                        'score': float(list(filter(None,request.POST.getlist('Diploma_Score[]')))[0]),
                        'score_unit': list(filter(None,request.POST.getlist('Diploma_Score_unit[]')))[0],
                        'start': datetime.strptime(list(filter(None,request.POST.getlist('Diploma_From[]')))[0], '%Y-%m'), 
                        'end': datetime.strptime(list(filter(None,request.POST.getlist('Diploma_To[]')))[0], '%Y-%m'),
                        'certificate': list(filter(None,request.POST.getlist('Diploma_Certi[]')))[0],
                        'is_current': False,
                    }

                except NotAvailable:
                    messages.error(request, 'Insufficient information for Diploma')
                    diploma = None
            # else:
            #     diploma = {
            #             'education': 'Diploma',
            #             'institute': '',
            #             'specialization': '',
            #             'board': '',
            #             'score': '',
            #             'score_unit': '',
            #             'start': datetime.strptime('0001-01', '%Y-%m'),
            #             'end': datetime.strptime('0001-01', '%Y-%m'),
            #             'certificate': 'Certificate not uploaded',
            #             'is_current': False,
            #         }
        
            X = None
            if len(list(filter(None,request.POST.getlist('X_School[]')))) > 0:
                try:
                    X = {
                        'education': 'X',
                        'institute': list(filter(None,request.POST.getlist('X_School[]')))[0],
                        'score': float(list(filter(None,request.POST.getlist('X_Score[]')))[0]),
                        'score_unit': list(filter(None,request.POST.getlist('X_Score_Unit[]')))[0],
                        'board': list(filter(None,request.POST.getlist('X_Board[]')))[0],
                        'start': datetime.strptime(list(filter(None,request.POST.getlist('X_From[]')))[0], '%Y-%m'),
                        'end': datetime.strptime(list(filter(None,request.POST.getlist('X_To[]')))[0], '%Y-%m'),
                        'certificate': list(filter(None,request.POST.getlist('X_Certi[]')))[0],
                        'is_current': False,
                        'specialization': 'General',
                    }

                except NotAvailable:
                    messages.error(request, 'Insufficient information for X')
                    X = None
            else:
                X = {
                        'education': 'X',
                        'institute': '',
                        'board': '',
                        'score': '',
                        'score_unit': '',
                        'start': datetime.strptime('0001-01', '%Y-%m'), 
                        'end': datetime.strptime('0001-01', '%Y-%m'),
                        'certificate': 'Certificate not uploaded',
                        'is_current': False,
                        'specialization': 'General',
                    }
            candidate_ref = db.collection('candidates').document(request.session['email']).get().to_dict()
            candidate_ref['education'] = list(filter(lambda x: True if x is not None else False, [X, XII, diploma]))

            institute = list(filter(None,request.POST.getlist('institute[]')))
            board = list(filter(None,request.POST.getlist('board[]')))
            From = list(filter(None,request.POST.getlist('from[]')))
            to = list(filter(None,request.POST.getlist('to[]')))
            grade = list(filter(None,request.POST.getlist('grade[]')))
            grade_of = list(filter(None,request.POST.getlist('grade-of[]')))
            qualification = list(filter(None,request.POST.getlist('qualification[]')))
            branch = list(filter(None,request.POST.getlist('branch[]')))
            certificate = list(filter(None,request.POST.getlist('othercerti[]')))
            education_det = list(zip(institute,board,From,to,grade,grade_of,qualification,branch,certificate))

            email = request.session['email']
            batch = list(db.collection(u'rel_batch_candidates').where(u'candidate_id', u'==', email).stream())[0]
            batch = batch.to_dict().get(u'batch_id')
            batch = db.collection(u'batches').document(batch).get().to_dict()

            college = batch['college']
            college = list(db.collection(u'users').where(u'college', u'==', college).stream())[0].to_dict()

            for institute, board, From , to, grade, grade_unit, quali, branch, certi in education_det:
                if institute == batch['college']:
                    continue
                course = { 'education' : quali,
                            'institute' : institute,
                            'specialization' : branch,
                            'board' : board,
                            'score' : float(grade),
                            'score_unit' : grade_unit,
                            'start' : datetime.strptime(From, '%Y-%m'),
                            'end' : datetime.strptime(to, '%Y-%m'),
                            'certificate' : certi,
                           'is_current': False,
                        }
                candidate_ref['education'].append(course)

            def score_unit(number):
                if number == 100:
                    return '%'
                else:
                    return '/' + str(number)

            current_ed = {
                'education': batch['course'],
                'board': college['board'],
                'certificate': None,
                'end': None,
                'institute': batch['college'],
                'score': list(request.POST.getlist('average_sem_score[]'))[0],
                'score_unit': score_unit(batch['grade']),
                'specialization': batch['branch'],
                'start': int(batch['batch_year'][:4]),
                'is_current': True,
                'sem_records': [],
                'total_live_backlogs': int(request.POST.getlist('total_live_backlogs[]')[0]),
                'total_closed_backlogs': int(request.POST.getlist('total_closed_backlogs[]')[0]),
            }

            semesters = []

            sem_score = list(request.POST.getlist('sem_score[]'))
            # print('scores', sem_score)
            sem_closed_backlog = list(request.POST.getlist('sem_closed_backlog[]'))
            # print('closed', sem_closed_backlog)
            sem_live_backlogs = list(request.POST.getlist('sem_live_backlogs[]'))
            # print('live', sem_live_backlogs)
            sem_certi = list(request.POST.getlist('semcerti[]'))
            # print('certi', sem_certi)
            sem_det = list(zip(sem_score, sem_closed_backlog, sem_live_backlogs, sem_certi))
            # print(sem_det)

            for sem, closed, live, certi in sem_det:
                semester = {
                    'semester_score': sem,
                    'closed_backlog': closed,
                    'live_backlog': live,
                    'certificate': certi
                }

                semesters.append(semester)

            # print(semesters)
            # return None
            current_ed['sem_records'] = semesters
            candidate_ref['education'].append(current_ed)

            update_data = dict()
            update_data['education'] = candidate_ref['education']
            update_data['total_certicount'] = request.POST.get('total_certicount')

        elif edit_type == 'add_exp':
            
            Exp_Type = list(filter(None,request.POST.getlist('expType[]')))
            Exp_Company = list(filter(None,request.POST.getlist('company[]')))
            Exp_from = list(filter(None,request.POST.getlist('from[]')))
            Exp_to = list(filter(None,request.POST.getlist('to[]')))
            Exp_desig = list(filter(None,request.POST.getlist('designation[]')))
            Exp_info = list(zip(list(filter(None,request.POST.getlist('info1[]'))),
                                list(filter(None,request.POST.getlist('info2[]'))),
                                list(filter(None,request.POST.getlist('info3[]')))))
            Exp_info = [shorten_info(info_) for info_ in Exp_info] #adding info in one line
            Exp_industry_type = list(filter(None,request.POST.getlist('industry_type[]')))
            Exp_domain = list(filter(None,request.POST.getlist('domain[]')))
            Exp_certi = list(filter(None,request.POST.getlist('certificate[]')))

            candidate_ref = db.collection('candidates').document(request.session['email']).get().to_dict()
            candidate_ref['experience'] = []

            training_det = list(zip(Exp_Type,Exp_Company,Exp_from,Exp_to,Exp_desig,Exp_info,Exp_industry_type,Exp_domain,Exp_certi))
            for Type,comp,From,to,desig,info,indus,domain,certi in training_det:
                course = { 'Type' : Type,
                            'company' : comp,
                            'from' : datetime.strptime(From, '%Y-%m'),
                            'to' : datetime.strptime(to, '%Y-%m'),
                            'designation' : desig,
                            'information' : info,
                            'industry' : indus,
                            'domain' : domain,
                            'certificate' : certi
                        }
                candidate_ref['experience'].append(course)
            update_data = dict()
            update_data['experience'] = candidate_ref['experience']
            update_data['total_certicount'] = request.POST.get('total_certicount')
            
        elif edit_type == 'add_proj':
            Project_Name = list(filter(None,request.POST.getlist('proName[]')))
            Project_Uni_or_Company = list(filter(None,request.POST.getlist('proUniversity[]')))
            Project_from = list(filter(None,request.POST.getlist('proForm[]')))
            Project_to = list(filter(None,request.POST.getlist('proTo[]')))
            Project_info = list(zip(list(filter(None,request.POST.getlist('proInfo1[]'))),
                                    list(filter(None,request.POST.getlist('proInfo2[]')))))
            Project_info = [shorten_info(info_) for info_ in Project_info] #adding info in one line
            Project_certi = list(filter(None,request.POST.getlist('procerti[]')))
            project_det = list(zip(Project_Name,Project_Uni_or_Company,Project_from,Project_to,Project_info,Project_certi))

            candidate_ref = db.collection('candidates').document(request.session['email']).get().to_dict()
            candidate_ref['projects'] = []

            for name,uni,From,to,info,certi in project_det:
                course = { 'Name' : name,
                            'University_Company' : uni,
                            'from' : datetime.strptime(From, '%Y-%m'),
                            'to' : datetime.strptime(to, '%Y-%m'),
                            'information' : info,
                            'certificate' : certi
                        }
                candidate_ref['projects'].append(course)
            
            update_data = dict()
            update_data['projects'] = candidate_ref['projects']
            update_data['total_certicount'] = request.POST.get('total_certicount')
            
        elif edit_type == 'add_lead':
            Leadership_Title = list(filter(None,request.POST.getlist('Role[]')))
            Leadership_organization = list(filter(None,request.POST.getlist('organization[]')))
            Leadership_from = list(filter(None,request.POST.getlist('from[]')))
            Leadership_to = list(filter(None,request.POST.getlist('to[]')))
            Leadership_info = list(zip(list(filter(None,request.POST.getlist('Info1[]'))),
                                        list(filter(None,request.POST.getlist('Info2[]'))) ))    
            Leadership_info = [shorten_info(info_) for info_ in Leadership_info] #adding info in one line
            Leadership_certi = list(filter(None,request.POST.getlist('Certificate[]')))

            candidate_ref = db.collection('candidates').document(request.session['email']).get().to_dict()
            candidate_ref['extra_curricular'] = []

            curricular_det = list(zip(Leadership_Title,Leadership_organization,Leadership_from,Leadership_to,Leadership_info,Leadership_certi))
            for role, org, From, to, info, certi in curricular_det:
                activity = {'role': role, 
                                'organisation': org,
                                'start': datetime.strptime(From, '%Y-%m'),
                                'end': datetime.strptime(to, '%Y-%m'),
                                'info': info,
                                'certificate' : certi
                                }
                candidate_ref['extra_curricular'].append(activity)
            
            update_data = dict()
            update_data['extra_curricular'] = candidate_ref['extra_curricular'] 
            update_data['total_certicount'] = request.POST.get('total_certicount')         

        elif edit_type == 'update_edu':
            candidate_ref = db.collection('candidates').document(request.session['email']).get().to_dict()
            update_data = dict()
            for education in candidate_ref['education']:
                if education['education'] == get_('init_edu'):
                    for field in education.keys():
                        education[field] = get_(field, education[field])
                    break

                update_data['education'] = candidate_ref['education']

        elif edit_type == 'del_exp':
            company = get_('company')
            designation = get_('designation')
            update_data = dict()
            candidate_ref = db.collection('candidates').document(request.session['email']).get().to_dict()
            experience = list(
                filter(lambda x: False if x['company'] == company and x['designation'] == designation else True,
                       candidate_ref['experience']))
            update_data['experience'] = experience

        elif edit_type == 'update_proj':
            candidate_ref = db.collection('candidates').document(request.session['email']).get().to_dict()
            update_data = dict()
            for project in candidate_ref['projects']:
                if project['name'] == get_('proNameInit'):
                    for field in project.keys():
                        project[field] = get_(field, project[field])
                    break

            update_data['projects'] = candidate_ref['projects']

        elif edit_type == 'del_pro':
            candidate_ref = db.collection('candidates').document(request.session['email']).get().to_dict()
            update_data = dict()
            projects = list(filter(lambda x: True if x['Name'] != get_('proName') else False,
                                   candidate_ref['projects']))
            update_data['projects'] = projects
        
        elif edit_type == 'del_lead':
            candidate_ref = db.collection('candidates').document(request.session['email']).get().to_dict()
            update_data = dict()
            lead = list(filter(lambda x: True if (x['role'] != get_('role') and x['organization'] != get_('comp') )  else False,
                                   candidate_ref['extra_curricular']))
            update_data['extra_curricular'] = lead

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
            awardDis = list(filter(None,request.POST.getlist('awardDis[]')))
            awardDate = list(filter(None,request.POST.getlist('awardDate[]')))
            awards = list(zip(awardDis,awardDate))
            candidate_ref = db.collection('candidates').document(request.session['email']).get().to_dict()
            candidate_ref['award'] = []
            for info, date in awards:
                award = {'description': info, 'date': datetime.strptime(date, '%Y-%m')}
                candidate_ref['award'].append(award)
            update_data = dict()
            update_data['award'] = candidate_ref['award']
           
        elif edit_type == 'add_skill':
            count = int(list(filter(None,request.POST.get('count')))[0])
            candidate_ref = db.collection('candidates').document(request.session['email']).get().to_dict()
            candidate_ref['skills'] = []
            update_data = dict()
            update_data['skills'] = []
            for i in range(0,count-1):
                dadict = []
                var = 'data['+str(i)+'][]'
                data = list(filter(None,request.POST.getlist(var)))
                name = data[0] #name of sub group
                subcount = int(data[1]) #count of skills in that group
                for j in range(0,subcount):
                    var1 = 'data['+str(i)+']['+str(j)+'][]'
                    sk = list(filter(None,request.POST.getlist(var1)))
                    dadict.append({sk[0] : sk[1]})
                update_data['skills'].append({name : dadict})
        elif edit_type == 'del_old_skill':
            gr = request.POST.get('group')
            sk = request.POST.get('skill')
            candidate_ref = db.collection('candidates').document(request.session['email']).get().to_dict()
            update_data = dict()
            for x in candidate_ref['skills']:
                if(list(x.keys())[0] == gr):
                    y = list(x.values())[0]
                    for z in y:  
                        if list(z.keys())[0] == sk:
                            y.remove(z)
                    candidate_ref['skills'].remove(x)
                    candidate_ref['skills'].append({gr : y})
            update_data['skills'] = candidate_ref['skills']    

        elif edit_type == 'del_old_skill_group':
            gr = request.POST.get('group')
            candidate_ref = db.collection('candidates').document(request.session['email']).get().to_dict()
            update_data = dict()
            for x in candidate_ref['skills']:
                if(list(x.keys())[0] == gr):
                    candidate_ref['skills'].remove(x)
            update_data['skills'] = candidate_ref['skills']    
            
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
            update_data = dict()
            for i, award in enumerate(exist_awards):
                desc, date = award['description'], award['date']
                if desc == des_init:
                    exist_awards.pop(i)
                    break

            update_data['award'] = exist_awards
        
        elif edit_type == 'del_skill':
            candidate_ref = db.collection('candidates').document(request.session['email']).get().to_dict()
            exist_skills = candidate_ref['skills']
            des_init = get_('skill')
            update_data = dict()
            for i, ski in enumerate(exist_skills):
                print(ski,i)
                if ski == des_init:
                    exist_skills.pop(ski)
                    break

            update_data['skills'] = exist_skills
        # print(request.session['email'])

        db.collection('candidates').document(request.session['email']).update(update_data)
        cand_dict = db.collection(u'candidates').document(request.session['email']).get().to_dict()

        link = generate_pdf(cand_dict)

        db.collection(u'candidates').document(request.session['email']).update({'pdfResume': link})

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
    saved={}
    
    save=db.collection(u'rel_candidate_savedjob').get()
    #applciations , applied and pending
    save_list=[]
    for k in save:
        save_list.append(k.to_dict()['job_id'])
    #print(save_list)
    for job_doc in docs:
        
        if job_doc.reference.collection('applicants').document(email).get().exists:
            req = db.collection('jobs').document(job_doc.id).get().to_dict()

            if 'company_name' not in req.keys():
                company_name = db.collection(u'users').document(req['email']).get().to_dict()['company_name']
                req['company_name'] = company_name

            #print(job_doc.id)
            if req is None:
                job_doc.reference.delete()
                continue

            status = job_doc.reference.collection('applicants').document(email).get().to_dict()['status']
            req['status'] = status
            

            if status == 'INCOMPLETE':
                pend_apps[job_doc.id] = req
            else:
                comp_apps[job_doc.id] = req

    #jobsdashboard view
    pendinglist= list(pend_apps.keys())
    completelist=list(comp_apps.keys())
    already_applied=completelist+pendinglist

    if request.session.get('hidename', None) is not None:
        return HttpResponseRedirect('/')

    cand_dict = db.collection(u'candidates').document(request.session['email']).get().to_dict()

    # TODO handle this redirection from JOBS to profile
    if 'freeze' in cand_dict.keys() and cand_dict['freeze']:
        messages.error(request, 'You cannot view any job posts')
        messages.error(request, 'You have been frozen by your training & placement officer')
        print('here')
        return redirect('/candidate/profile')

    placements = db.collection(u'rel_placement_candidates').where(
        u'candidate_id', u'==', request.session['email']).get()
    placements = [placement.to_dict()['placement_id'] for placement in placements]

    job_ids = list()
    for id_ in placements:
        jobs = db.collection(u'rel_placement_jobs').where(
            u'placement_id', u'==', id_).where(u'status', u'==', u'open').get()
        jobs = [doc.to_dict()['job_id'] for doc in jobs]
        job_ids += jobs

    job_ids = list(set(job_ids))
    # print(job_ids)
    job_docs = [db.collection(u'jobs').document(id_).get() for id_ in job_ids]

    def closed_filter(doc):
        try:
            deadline = doc.to_dict()['deadline']
        except KeyError:
            return False
        if datetime.strptime(deadline, '%Y-%m-%d') < datetime.now():
            return False
        else:
            return True

    def already_applied_filter(doc):
        if doc.reference.id in already_applied: 
            return False
        else:
            return True
    #data error
    for doc in job_docs:
        # TODO
        if datetime.strptime(doc.to_dict()['deadline'], '%Y-%m-%d') < datetime.now():
            doc.to_dict()['status'] = 'Closed'
            db.collection('jobs').document(doc.reference.id).update({'status': 'Closed'})
    job_docs = list(filter(closed_filter, job_docs))
    job_docs = list(filter(already_applied_filter, job_docs))
    company_jobs = []

    # counting the number of jobs by 'post' and storing it in jobs_count
    jobs_opnd = {}
    jobs_count = {}
    for job in job_docs:
        # appeding the details of the job to the jobs_opnd list.
        jobs_opnd[job.id.strip()] = job.to_dict()
        try:
            if 'by_campus' in job.to_dict().keys():
                jobs_opnd[job.id.strip()]['cmpnm'] = db.collection(u'users').document(
                    job.to_dict()['email']).get().to_dict()['college']
            else:
                jobs_opnd[job.id.strip()]["cmpnm"] = db.collection(u'users').document(
                    job.to_dict()['email']).get().to_dict()['company_name']
        except TypeError:
            db.collection(u'jobs').document(job.id).delete()
            db.collection(u'applications').document(job.id).delete()
            rels = db.collection(u'rel_placement_jobs').where(u'job_id', u'==', job.id).get()

            for rel in rels:
                rel.reference.delete()
            continue

        # appending the job-id's to the company_jobs array.
        # the logic for counting the number of jobs postwise.
        company_jobs.append(job.id.strip())
        if not str(job.to_dict()['post']) in jobs_count:
            jobs_count[str(job.to_dict()['post'])] = 1
        else:
            jobs_count[str(job.to_dict()['post'])] += 1

        if(job.id in save_list):
            #print(job.id)
            saved[job.id]=jobs_opnd[job.id]
    # comment out the lines in case you want to see the data by yourself.

    # sort all lists by timestamps
    jobs_opnd = list(jobs_opnd.items())
    comp_apps = list(comp_apps.items())
    pend_apps = list(pend_apps.items())
    saved = list(saved.items())

    print(pend_apps)
    # print(jobs_opnd[0], comp_apps[0], pend_apps[0], saved[0])
    for list_ in [jobs_opnd, comp_apps, pend_apps, saved]:
        list_.sort(key=lambda x: x[1]['timestamp'], reverse=True)

        for id_, info in list_:
            info['place'] = info.get('place', '-')
            info['cmpnm'] = info.get('cmpnm', info.get('company_name', '-'))
    return render(request, 'candidate/applications.html', {'comp_apps': comp_apps,
                                                           'pend_apps': pend_apps,
                                                           'jobsss': jobs_opnd,
                                                           'saved':saved,
                                                           'lapp':len(comp_apps),
                                                           'lpen': len(pend_apps),
                                                           'saved_list':save_list,
                                                           }
                  )


def saved(request):
    if request.method == 'POST':
        #print("hey")
        id=request.POST.get('id')
        #print(request.session['email'])
        #print(id)
        docs=db.collection('rel_candidate_savedjob').where(u'job_id',u'==',id).where(u'cand_id',u'==',request.session['email']).get()
        x=None
        for doc in docs:
            #print(doc)
            x=doc
        
        if x==None:
            data={'cand_id':request.session['email'],'job_id':id}
            #print(data)
            db.collection('rel_candidate_savedjob').document().set(data)
        else:
            rels=db.collection('rel_candidate_savedjob').where(u'job_id',u'==',id).where(u'cand_id',u'==',request.session['email']).get()
            for rel in rels:
                rel.reference.delete()
            
        return JsonResponse({'success': 'True'})
'''

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
            print(update_data, "pri")

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

            if 'education' in candidate_ref.keys():
                exist_education = [x['education'] for x in candidate_ref['education']]
            else:
                exist_education = []
                candidate_ref['education'] = []

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

            if 'experience' in candidate_ref.keys():
                exist_exp = [(x['company'], x['designation']) for x in candidate_ref['experience']]
            else:
                exist_exp = []
                candidate_ref['experience'] = []

            for company, designation, from_, to, info, type_ in training_det:
                if (company, designation) not in exist_exp:
                    internship = {'company': company.strip(), 'designation': designation.strip(),
                                  'from': from_, 'to': to, 'info': info, 'type': type_}
                    candidate_ref['experience'].append(internship)

            update_data['experience'] = candidate_ref['experience']

        elif edit_type == 'add_proj':
            # print(request.POST)
            # (name, info, date)
            # print(request.POST.getlist('proName[]')[::-1], )
            project_det = list(zip(request.POST.getlist('proName[]')[::-1], request.POST.getlist('proDis[]')[::-1],
                                   request.POST.getlist('proDate[]')[::-1]))

            # print(project_det)

            project_det = list(filter(null_filter, project_det))
            candidate_ref = db.collection('candidates').document(request.session['email']).get().to_dict()

            if 'projects' in candidate_ref.keys():
                exist_proj = [x['name'] for x in candidate_ref['projects']]
            else:
                exist_proj = []
                candidate_ref['projects'] = []

            # print(exist_proj)

            for name, info, date in project_det:
                if name not in exist_proj:
                    project = {'name': name.strip(), 'info': info.strip(), 'date': date.strip()}
                    candidate_ref['projects'].append(project)

            update_data['projects'] = candidate_ref['projects']
            # print(update_data['projects'])

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
            experience = list(
                filter(lambda x: False if x['company'] == company and x['designation'] == designation else True,
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

            if 'award' in candidate_ref.keys():
                exist_awards = set([
                    (award['description'], award['date']) for award in candidate_ref['award']
                ])
            else:
                exist_awards = set([])
                candidate_ref['award'] = []

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
'''




def jobInterview(request, ifext=False):
    if request.method == 'POST':
        # print(request.POST)
        if ifext:
            jobId = request.session.get('job_id')
        else:
            jobId = request.POST['job'].strip()
        # print(jobId)
        candidate = request.session.get('email')
        candidate_dict = db.collection('candidates').document(candidate).get().to_dict()

        if not db.collection(u'applications').document(jobId).collection(u'applicants').document(
                candidate).get().exists:
            job_doc = db.collection(u'jobs').document(jobId).get().to_dict()

            add_questions_coll = False

            if db.collection(u'applications').document(jobId).get().exists and list(db.collection(
                    'applications').document(jobId).collection('questions').get()):
                questions_coll = db.collection(u'applications').document(jobId).collection(u'questions').get()
            else:
                add_questions_coll = True
                questions_coll = db.collection(u'users').document(job_doc['email']).collection(u'packages').document(
                    job_doc['packageId']).collection(u'questions').get()

            questions_coll = list(questions_coll)

            que = []
            for q in questions_coll:
                que.append(q.to_dict())

            db.collection(u'applications').document(jobId).set({})

            # if job_doc['applicat_req']['vid_interview']:
            # questions_coll = db.collection(u'users').document(job_doc['email']).collection(u'packages').document(
            #     job_doc['packageId']).collection(u'questions').get()

            if add_questions_coll:
                for ques_doc in questions_coll:
                    db.collection('applications').document(jobId).collection('questions').document(
                        ques_doc.id).set(ques_doc.to_dict())

            db.collection(u'applications').document(jobId).collection(u'applicants').document(candidate).set({
                'candidate_name': candidate_dict['name'],
                'status': "INCOMPLETE",
                'video_interview_links': {},
                'resume_score': "7",
                'video_resume_score': "6",
                'skills_score': {'a': 4, 'c': 3, 'e': 5, 'n': 5, 'o': 3},
                'grades': {'1': 3, '2': 6, '3': 6, '4': 5},
                'timestamp': datetime.now(),
            })

            # increment_link_count(jobId, )
            thank_vid = db.collection('users').document(job_doc['email']).get().to_dict()['thank_vid']
            # thank_vid = company['thank_vid']

            return render(request, 'candidate/job_interview.html',
                          {'jobId': jobId, 'job': job_doc, 'questions': que, 'startFrom': 0, 'thank_vid': thank_vid})
        else:
            ap = db.collection(u'applications').document(jobId).collection(u'applicants').document(candidate).get()
            apdic = ap.to_dict()
            if apdic['status'] == 'INCOMPLETE':
                job_doc = db.collection(u'jobs').document(jobId).get().to_dict()
                questions = db.collection(u'users').document(job_doc['email']).collection(u'packages').document(
                    job_doc['packageId']).collection(u'questions').get()
                que = []
                for q in questions:
                    que.append(q.to_dict())
                d = {k: v for k, v in apdic['video_interview_links'].items() if v != ""}
                startFrom = len(d)
                messages.success(request, 'Continue the mock interview')
                # print("lmao bruh")
                thank_vid = db.collection('users').document(job_doc['email']).get().to_dict().get('thank_vid', settings.DEFAULT_THANK_VID)

                return render(request, 'candidate/job_interview.html',
                              {'jobId': jobId, 'job': job_doc, 'questions': que, 'startFrom': startFrom,
                               'thank_vid': thank_vid})
            if apdic['status'] == 'UNREVIEWED':
                messages.success(request, 'Your Application will be soon reviewed.')
                add_application(jobId, candidate, {}, web_db=db)
                return redirect('/candidates/applications')
    else:
        return HttpResponseRedirect('applications')


def addApplication(request):
    print(request.POST)
    type = request.POST.get('type')
    if type == 'final':
        candidate = request.session.get('email')
        job = request.POST.get('job')
        add_application(job, candidate, {'status': 'UNREVIEWED'}, web_db=db)
        # db.collection(u'applications').document(job).collection(u'applicants').document(candidate).update({
        #     'status': "UNREVIEWED"
        # })
        messages.success(request, 'Application added successfully.')
        job_doc = db.collection('jobs').document(request.POST.get('job')).get().to_dict()
        remove_saved_job_relation(job,candidate)
        log_notification(type_='cand_applied', post=job_doc['post'],
                         rec_email=job_doc['email'], job_id=request.POST.get('job'))
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

        # messages.success(request, 'Application added successfully.')
        # job_doc = db.collection('jobs').document(request.POST.get('job')).get().to_dict()
        
        # log_notification(type_='cand_applied', post=job_doc['post'],
                        #  rec_email=job_doc['email'], job_id=request.POST.get('job'))
        return JsonResponse({"success": "True"})


def introduction(request):
    que = "tell me about yourself"
    return render(request, 'candidate/introduction.html', {'questions': que, 'startFrom': 0})



def new_application(request):
    if request.method == 'POST':
        job_id = request.POST['job'].strip()
        cand_doc = db.collection('candidates').document(request.session['email']).get().to_dict()
        job_doc = db.collection('jobs').document(job_id).get().to_dict()

        if db.collection('applications').document(job_id).collection('applicants').document(
                request.session['email']).get().exists:
            messages.error(request, 'You have already applied for this job')
            return redirect('applications')

        if job_doc['status'] == 'Closed':
            messages.error(request, 'The last date to apply has passed')
            return redirect('applications')

        if cand_doc['profile_status'] == 'empty':
            messages.error(request, 'Please complete basic profile first')
            return redirect('applications')

        if 'applicat_req' not in job_doc.keys():
            job_doc['applicat_req'] = {
                'vid_resume': False,
                'personality_ques': False,
                'vid_interview': False,
                }

        if cand_doc['profile_status'] == 'partial':
            if cand_doc.get('pdfResume') is None:
                messages.error(request, 'Please upload your resume first')
                return redirect('resume_upload')

            elif cand_doc.get('video_resume') is None and job_doc['applicat_req']['vid_resume']:
                messages.error(request, 'You are required to upload video resume to apply for this job')
                return redirect('videoResume')

            elif cand_doc.get('psycho_ques') is None and job_doc['applicat_req']['personality_ques']:
                messages.error(request, 'You are required to complete psychology test to apply for this job')
                return redirect('psychology')
            else:
                pass

        application = {
            'candidate_name': cand_doc['name'],
            'grades': {'1': 3, '2': 3, '3': 8, '4': 5},
            'pdfResume': cand_doc['pdfResume'],
            'resume_score': 7,
            'skills_score': {'o': 3, 'c': 3, 'e': 2, 'a': 5, 'n': 1},
            'status': None,
            'timestamp': datetime.now(),
            'video_interview_links': dict(),
            'video_resume_score': 5,
        }

        if job_doc['applicat_req']['vid_resume']:
            application['video_resume'] = cand_doc['video_resume']

        if job_doc['applicat_req']['personality_ques']:
            application['psycho_ques'] = cand_doc['psycho_ques']

        if not job_doc['applicat_req']['vid_interview']:
            application['status'] = 'UNREVIEWED'

            if 'email_message' not in job_doc.keys() or 'email_subject' not in job_doc.keys():
                add_application(job_id, request.session['email'], application, email=False, web_db=db)
            else:
                add_application(job_id, request.session['email'], application, web_db=db)
            #remove saved, testing remain
            remove_saved_job_relation(job_id,request.session['email'])

            messages.success(request, 'You have successfully applied')
            log_notification(type_='cand_applied', post=job_doc['post'], rec_email=job_doc['email'],
                             job_id=job_id)
            return redirect('applications')
        else:
            application['status'] = 'INCOMPLETE'
            add_application(job_id, request.session['email'], application, email=False, web_db=db)
            request.session['job_id'] = job_id
            return jobInterview(request, True)



def resume_upload(request):
    if request.method == 'GET':
        context = dict()
        return render(request, 'candidate/resume_upload.html', context)
    else:
        cand_id = request.session['email']
        cand_doc = db.collection(u'candidates').document(cand_id).get().to_dict()
        status = 'partial'

        if cand_doc.get('video_resume') is not None and cand_doc.get('psycho_ques') is not None:
            status = 'complete'

        db.collection(u'candidates').document(cand_id).update(
            {'pdfResume': request.POST.get('link'), 'profile_status': status})

        return JsonResponse({'success': True})


def generate_pdf(candidate_dict):
    """
    creates pdf resume and uploads it on firebase
    :param candidate_dict: profile data of the candidate
    :return: link to pdfResume
    :rtype: str
    """
    # change activity format
    for activity in candidate_dict['extra_curricular']:
        activity['start'] = activity['start'].strftime("%b'%y")
        activity['end'] = activity['end'].strftime("%b'%y")

    # process the data
    data = jsonParser.jsonParser(candidate_dict)

    # create pdf at 'media/temp/create_resume'
    isme.generate_pdf(data)

    # upload the resume to firebase
    from firebase_admin import storage
    import os

    bucket = storage.bucket()
    pdf_name = candidate_dict['First_name'] + '_' + candidate_dict['Last_name'] + '.pdf'
    blob = bucket.blob('candidate_resumes/' + pdf_name)
    blob.make_public()
    blob.upload_from_filename('media/temp/create_resume/' + candidate_dict['First_name'] + ' ' + candidate_dict['Last_name'] + '.pdf')
    link = blob.public_url

    # download_link = blob.media_link

    # remove file from local storage
    os.remove('media/temp/create_resume/' + candidate_dict['First_name'] + ' ' + candidate_dict['Last_name'] + '.pdf')

    return link


