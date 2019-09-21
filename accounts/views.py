from django.shortcuts import render
from django.http import HttpResponse

def login(request):
    return render(request,'accounts/login.html')

def candidate_signup(request):
    return render(request,'accounts/candidate_signup.html')

def recruiter_signup(request):
    return render(request,'accounts/recruiter_signup.html')
