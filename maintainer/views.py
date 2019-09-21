from django.shortcuts import render
from django.http import HttpResponse

def dashboard(request):
    return render(request,'maintainer/dashboard.html')