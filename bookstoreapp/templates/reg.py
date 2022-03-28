from django.core.checks import messages
from django.contrib import messages
#from django.http import response,Http404
from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User,auth
#from django.conf import settings
#from django.conf.urls.static import static


# Create your views here.
def index(request):
    return render(request,"index.html")

def login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('user/userindexpage')
        else:
            messages.info(request,'invalid credentials')
            return redirect('registration/loginpage')
    return render(request,"registration/login.html")

def register(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        if password==password:
            if User.objects.filter(username=username).exists():
                #messages.info('username already taken')
                return redirect('registration/loginpage')
            else:
                user=User.objects.create_user(username=username,password=password)
                user.save()
                return redirect('registration/loginpage')
        else:
            #messages.info('password is not matching...')
            return redirect('registration/loginpage')
    return render(request,'registration/login.html')
def registerr(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        if password==password:
            if User.objects.filter(username=username).exists():
                #messages.info('username already taken')
                return redirect('registration/loginpage')
            else:
                user=User.objects.create_user(username=username,password=password)
                user.save()
                return redirect('registration/registerpage')
        else:
            #messages.info('password is not matching...')
            return redirect('registration/registerpage')
    return render(request,'registration/login.html')
    #return render(request,"registration/register.html")



    
def librarianindex(request):
    #data=Book.objects.all()
    return render(request,"librarian/librarianindex.html")


def userindex(request):
    #data=Book.objects.all()
    return render(request,"user/userindex.html")