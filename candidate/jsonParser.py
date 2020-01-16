def jsonParser(jsondata):
    # jsondata = jsondata["candidate"]
    parseData = {}

    '''academics'''
    try:
        education_table = []
        education_table.append(
            ['Qualification/Certification', 'School/Institute', 'Board/University', 'Year', 'Marks(%)'])
        for each_row in jsondata["education"]:
            newrow = []
            if "score" in each_row.keys():
                newrow.extend(['{}'.format(each_row.setdefault('education', '-')),
                               '{}'.format(each_row.setdefault('institute', '-')),
                               '{}'.format(each_row.setdefault('board', '-')),
                               '{} {}'.format(each_row.setdefault('score', '-'), each_row.setdefault('score_unit', '-'))
                               ])
                try:
                    dates = each_row['end'].strftime("%b'%y")
                except AttributeError:
                    dates = '{}'.format('   -  ')
                newrow.insert(3, dates)
                education_table.append(newrow)
        parseData["Academic Qualification"] = education_table
    except (KeyError, AttributeError, TypeError) as e:
        parseData["Academic Qualification"] = None
        print("Academic detatils error", e)
        pass

    '''experience'''
    try:
        experience_table = []
        for each_row in jsondata["experience"]:
            newrow = []
            each_row['from'] = each_row['from'].strftime("%b'%y")
            each_row['to'] = each_row['to'].strftime("%b'%y")
            newrow.extend(['<b>{}</b>'.format(each_row.setdefault('company', '-')),
                           '<i>{}</i>'.format(each_row.setdefault('designation', '-')),
                           '<b>[{}-{}]</b>'.format(each_row['from'], each_row['to'])
                           ])
            newrow.extend(each_row["information"])
            experience_table.append(newrow)
        parseData["Professional Experience"] = experience_table
    except (KeyError, AttributeError) as e:
        parseData["Professional Experience"] = None
        print("Experinence detatils error", e)
        pass

    '''projects'''
    try:
        project_table = []
        for each_row in jsondata["projects"]:
            newrow = []
            each_row['from'] = each_row['from'].strftime("%b'%y")
            each_row['to'] = each_row['to'].strftime("%b'%y")
            newrow.extend([
                '<b>{} | {}</b>'.format(each_row.setdefault('Name', '-'),
                                        each_row.setdefault('University_Company', '-')),
                '<b>[{}-{}]</b>'.format(each_row['from'], each_row['to']),
            ])
            newrow.extend(each_row["information"])
            project_table.append(newrow)
        parseData["Academic / Industrial Projects"] = project_table
    except (KeyError, AttributeError) as e:
        parseData["Academic / Industrial Projects"] = None
        print("Projects detatils error", e)
        pass

    ''' extra curricular'''
    try:
        extra_curricular_table = []
        for each_row in jsondata["extra_curricular"]:
            newrow = []
            newrow.extend([
                '<b>{} | {}</b>'.format(each_row.setdefault('role', '-'), each_row.setdefault('organisation', '-')),
                '<b>{} | {}</b>'.format(each_row.setdefault('start', '-'), each_row.setdefault('end', '-')),
            ])
            newrow.extend(each_row['info'])
            extra_curricular_table.append(newrow)
        parseData['Extracurricular Activities'] = extra_curricular_table
    except (KeyError, AttributeError) as e:
        parseData['Extracurricular Activities'] = None
        print("Extra Curricular detatils error", e)
        pass

    try:
        parseData["name"] = jsondata["First_name"] + " " + jsondata["Last_name"]
    except (KeyError, AttributeError) as e:
        print("Error in name field:", e)
        pass

    try:
        parseData["gender"] = jsondata["gender"]
    except (KeyError, AttributeError) as e:
        print("Error in gender field:", e)
        pass

    try:
        parseData["email"] = jsondata["email"]
    except (KeyError, AttributeError) as e:
        print("Error in Email field", e)
        pass

    try:
        parseData["phone_no"] = '{}'.format(jsondata["ph_no"])
    except (KeyError, AttributeError) as e:
        print("Error in phone number field", e)
        pass

    try:
        parseData["Roll_No"] = jsondata["roll_no"]
    except (KeyError, AttributeError) as e:
        print("Error in Roll No field", e)
        pass

    try:
        parseData["DOB"] = jsondata['dob']
    except (KeyError, AttributeError) as e:
        print("Error in DOB field", e)
        pass

    ''' skills '''
    try:
        skill_table = []
        for each_row in jsondata['skills']:
            skill_and_level = ''
            category = list(each_row.keys())[0]
            skill_and_level += ''.join(category)
            skill_and_level += ' : '
            for each_skill in each_row[category]:
                skill_key = list(each_skill.keys())[0]
                skill_and_level += skill_key
                skill_and_level += ' ('
                skill_and_level += each_skill[skill_key]
                skill_and_level += '),'
            skill_table.append(skill_and_level)
        parseData['Skills'] = [skill_table]
    except (KeyError, AttributeError) as e:
        parseData['Skills'] = None
        print("Skill detatils error", e)
        pass

    ''' awards and Certification '''
    try:
        awards_table = []
        for each_row in jsondata['award']:
            newrow = []
            each_row['date'] = each_row['date'].strftime("%b'%y")
            newrow.append([
                '{}'.format(each_row['description']),
                '<b>[{}]</b>'.format(each_row['date'])
            ])
            awards_table.extend(newrow)
        parseData['Awards'] = awards_table
    except (KeyError, AttributeError) as e:
        parseData['Awards'] = None
        print("Awards and Certification detatils error", e)
        pass

    return parseData
