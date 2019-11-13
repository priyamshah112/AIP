from django.shortcuts import render
from django.http import HttpResponse

def view_jobs(request):
    return render(request,'candidate/view_jobs.html')

def jobs_board(request):
    return render(request,'candidate/jobs_board.html')

def candidate_signup(request):
    return render(request,'candidate/candidate signup.html')

def edit_profile(request):
    return render(request,'candidate/edit.html')
    
def applied(request):
    return render(request,'candidate/applied.html')
