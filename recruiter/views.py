from django.shortcuts import render
from django.http import HttpResponse

def jobs(request):
    return render(request,'recruiter/jobs.html')