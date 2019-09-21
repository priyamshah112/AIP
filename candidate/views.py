from django.shortcuts import render
from django.http import HttpResponse

def view_jobs(request):
    return render(request,'candidate/view_jobs.html')