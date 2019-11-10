from django.shortcuts import render
from django.http import HttpResponse



def index(request):
    return render(request,'AIP/index.html')

def nav(request):
    return render(request,'AIP/nav.html')

def login(request):
    return render(request,'AIP/signin.html')


def candidate_signup(request):
    return render(request,'candidate/candidate signup.html')


def recruiter_signup(request):
    return render(request,'recruiter/recruiter signup.html')

