from ibm_watson import PersonalityInsightsV3
from ibm_watson import ApiException
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import json
import speech_recognition as sr 
import moviepy.editor as mp
import time
from subprocess import Popen, PIPE
import os
import requests
from firebase_admin import firestore
from django.conf import settings
import math
db = firestore.client()

def personality_insights(candidate,job,ids,que,video_path):
  try:
    path = settings.BASE_DIR + '/media/'+candidate+'/'

    # if no such folder exists, creates an empty folder
    if not os.path.exists(path):
        os.makedirs(path)
        print("folder created ", path)

    r1 = requests.get(video_path)
    inp = path+ids+'.webm'
    print(inp)
    with open(inp,"wb") as f:
        f.write(r1.content)
    print("writing video in file")
    time.sleep(3)
    print("preprocessing personality insights algorithm")
    video_path = inp
    video_path = os.path.splitext(video_path)[0]
    print(video_path)
    r = "ffmpeg -i "+video_path+".webm "+video_path+".mp4"
    print(r)
    p1 = Popen(r,shell=True)
    print(p1.communicate())
    time.sleep(5)
    print("sleeping done conversion")
    video_path+=".mp4"
    print("final ",video_path)
    a = time.time()
    # Video to Audio 

    clip = mp.VideoFileClip(video_path) #.mp4 path
    video_wav = path+ids+".wav"
    clip.audio.write_audiofile(video_wav) #.wav path

    b = time.time()
    print("Video to Audio Processing time : ",(b-a))

    # # Audio to Text

    AUDIO_FILE = (video_wav) #.wav path  
    r = sr.Recognizer() 
        
    with sr.AudioFile(AUDIO_FILE) as source: 
        audio = r.record(source)   
        
    try: 
        temp = r.recognize_google(audio,language="en-US")
        print(temp)
        pp = path+"mywords.txt"
        with open(pp,'a') as w:
            w.write(temp)
        cp = path+"profile.json"
        f = open(pp,'r')
        cptext = f.read()
        print("profile.json path ",cp)
        with open(cp,'w') as w:
            w.write('{"contentItems": [{"content": "'+cptext+'","contenttype": "text/plain","created":1447639154000,"id": "666073008692314113","language": "en"}]}')

    except sr.UnknownValueError: 
        print("Google Speech Recognition could not understand audio")
        exit()
        
    except sr.RequestError as e: 
        print("Could not request results from Google Speech  Recognition service; {0}".format(e)) 
        exit()

    c = time.time()
    print("Audio to text processing time : ",(c-b))

    # Personality Insights
    try:
        authenticator = IAMAuthenticator('Y4FpG4YE1huEfu02JwYsZoVQfpQvttGVRJJZl6t3jIlz')
        personality_insights = PersonalityInsightsV3(
            version='2017-10-13',
            authenticator=authenticator
        )

        personality_insights.set_service_url('https://gateway-lon.watsonplatform.net/personality-insights/api')

        with open(cp) as profile_json:
            profile = personality_insights.profile(
                profile_json.read(),
                'application/json',
                content_type='application/json',
                consumption_preferences=True,
                raw_scores=True
            ).get_result()

        print(json.dumps(profile, indent=2))


        print("*****************************")
        p = json.loads(json.dumps(profile, indent=2))
        print(p['personality'][0]['name'])
        print(float(p['personality'][0]['percentile'])*100)
        print(p['personality'][1]['name'])
        print(float(p['personality'][1]['percentile'])*100)  
        print(p['personality'][2]['name'])
        print(float(p['personality'][2]['percentile'])*100)
        print(p['personality'][3]['name'])
        print(float(p['personality'][3]['percentile'])*100)  
        print(p['personality'][4]['name'])
        print(float(p['personality'][4]['percentile'])*100)  
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        score = [int(math.ceil((float(p['personality'][0]['percentile'])*10)/2)) , int(math.ceil((float(p['personality'][1]['percentile'])*10)/2)) ,int(math.ceil((float(p['personality'][2]['percentile'])*10)/2)) ,int(math.ceil((float(p['personality'][3]['percentile'])*10)/2)) ,int(math.ceil((float(p['personality'][4]['percentile'])*10)/2))]
        print(score)
        doc_ref = db.collection(u'applications').document(job).collection(u'applicants').document(candidate)
        vd_dic = doc_ref.get().to_dict()['video_interview_score']
        vd_dic.update({ids: score})
        doc_ref.update({
            'video_interview_score': vd_dic
        })
        #print(json.loads(json.dumps(profile, indent=2))['personality']["percentile"])
    except ApiException as ex:
        print("Method failed with status code " + str(ex.code) + ""+ ex.message)

        p = 0 # error can't calc personality

    d = time.time()
    print("Overall Processing Time : ",(d-a))
  
  except Exception as e:
      print("algo complete failure personality ",e)
      score = [0,0,0,0,0]
      print(score)
      doc_ref = db.collection(u'applications').document(job).collection(u'applicants').document(candidate)
      vd_dic = doc_ref.get().to_dict()['video_interview_score']
      vd_dic.update({ids: score})
      doc_ref.update({
        'video_interview_score': vd_dic
      })      
  #return float(p['personality'][0]['percentile'])*100,float(p['personality'][1]['percentile'])*100,float(p['personality'][2]['percentile'])*100,float(p['personality'][3]['percentile'])*100,float(p['personality'][4]['percentile'])*100


#print(personality_insights("video.mp4"))
