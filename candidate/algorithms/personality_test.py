from ibm_watson import PersonalityInsightsV3
from ibm_watson import ApiException
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import json
import speech_recognition as sr 
import moviepy.editor as mp
import time


def personality_insights(video_path):
  a = time.time()
  # Video to Audio 

  clip = mp.VideoFileClip(video_path) #.mp4 path
  video_wav = 'temp.wav'
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
      with open("profile.json",'w') as w:
        w.write('{"contentItems": [{"content": "'+temp+'","contenttype": "text/plain","created":1447639154000,"id": "666073008692314113","language": "en"}]}')

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

    with open('profile.json') as profile_json:
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
    #print(json.loads(json.dumps(profile, indent=2))['personality']["percentile"])
  except ApiException as ex:
      print("Method failed with status code " + str(ex.code) + ""+ ex.message)

      p = 0 # error can't calc personality

  d = time.time()
  print("Overall Processing Time : ",(d-a))

  return float(p['personality'][0]['percentile'])*100,float(p['personality'][1]['percentile'])*100,float(p['personality'][2]['percentile'])*100,float(p['personality'][3]['percentile'])*100,float(p['personality'][4]['percentile'])*100

print(personality_insights("Ans1.mp4"))