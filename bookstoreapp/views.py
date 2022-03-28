from django.core.checks import messages
from django.contrib import messages
#from django.http import response,Http404
from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User,auth
from .models import Book
#from.form import EditForm
from django.contrib.auth.decorators import login_required
#from django.conf import settings
#from django.conf.urls.static import static
import os


# Create your views here.
def index(request):
    return render(request,"index.html")

def login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=auth.authenticate(username=username,password=password)
        print(user)
        if username == 'admin':
            return redirect('librarian/librarianindex')
        if user is not None:
            auth.login(request,user)
            return redirect('user/userindexpage')
        else:
            messages.info(request,'invalid credentials')
            return redirect('registration/loginpage')
    return render(request,"registration/login.html")

def registerr(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        password2=request.POST['password2']
        
        if password==password2:
            if User.objects.filter(username=username).exists():
                messages.info(request,'username already taken')
                return redirect('registration/loginpage')
            else:
                user=User.objects.create_user(username=username,password=password)
                user.save()
                return redirect('registration/loginpage')
        else:
            messages.info(request,'password is not matching...')
            return redirect('registration/registerpage')
    return render(request,'registration/register.html')
    
#librarian indexpage
@login_required
def librarianindex(request):
    data=Book.objects.all()
    return render(request,"librarian/librarianindex.html",{'obj':data})


#userindex page
@login_required
def userindex(request):
    data=Book.objects.all()
    return render(request,"user/userindex.html",{'obj':data})


#for adding book

def addbook(request):
    if request.method=='POST':
        name=request.POST.get('name')
        author=request.POST.get('author')
        desc=request.POST.get('desc')
        pdf=request.FILES.get('pdf')
        obj=Book()
        obj.name=name
        obj.author=author
        obj.desc=desc
        obj.pdf=pdf
        obj.save()
        return redirect(librarianindex)
    else:
        return render(request,"librarian/addbook.html")
    

#editing form


def editbook(request, pk):
    data = Book.objects.get(id=pk)

    if request.method == "POST":
        if len(request.FILES) != 0:
            if len(data.pdf) > 0:
                os.remove(data.pdf.path)
            data.pdf = request.FILES['pdf']
        data.name = request.POST.get('name')
        data.author = request.POST.get('author')
        data.desc = request.POST.get('desc')
        data.save()
        messages.success(request, " Updated Successfully")
        return redirect(librarianindex)

    context = {'data':data}
    return render(request, 'librarian/editbook.html', context)
#editing form 

'''def updatedata(request,id):
    data=Book.objects.get(id=id)
    form=EditForm(instance=data)
    if request.method=="POST":
        form=EditForm(request.POST,instance=data)
        if form.is_valid():
            form.save()
            return redirect(librarianindex)    
    return render(request,"librarian/editbook.html",{'form':form})'''


#deleting data from form

def deletedata(request,id):
    data=Book.objects.get(id=id)
    data.delete()
    return redirect(librarianindex)

