from pyexpat import model
from django.core.checks import messages
from django.contrib import messages
#from django.http import response,Http404
from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User,auth
from .models import Book
from django.contrib.auth.decorators import login_required
from django.conf import settings
#from django.conf.urls.static import static
from.form import EditForm
import os
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views import View
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView

# Create your views here.
class Index(TemplateView):
    template_name = "index.html"

#class based view for login page
class LoginView(View):
    def get(self,request):
        return render(request,"registration/login.html")
    def post(self,request):
        username=request.POST['username']
        password=request.POST['password']
        user=auth.authenticate(username=username,password=password)
        #print(user)
        if username == 'admin@gmail.com':
            return redirect('librarian/librarianindex')
        if user is not None:
            auth.login(request,user)
            send_mail('Login successful','Welcome to our mini bookstore!!',settings.EMAIL_HOST_USER,[username])
            return redirect('user/userindexpage')
        else:
            messages.info(request,'invalid credentials')
            return redirect('registration/loginpage')

#class based view for registration
class RegisterView(View):
    def get(self,request):
        return render(request,"registration/register.html")
    def post(self,request):
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
                send_mail('Registration successful','Login to see more!!',settings.EMAIL_HOST_USER,[username])
                return redirect('registration/loginpage')
        else:
            messages.info(request,'password is not matching...')
            return redirect('registration/registerpage')

#class based view for viewing index page
class LibrarianIndexView(ListView):
    model=Book
    template_name="librarian/librarianindex.html"
    context_object_name='obj'

#class based view for userindexpage
class UserIndexView(ListView):
    model=Book
    template_name="user/userindex.html"
    context_object_name='obj'

#class based view for adding a book
class AddBook(View):
    def get(self,request):
       return render(request,"librarian/addbook.html") 
    def post(self,request):
        name=request.POST.get('name')
        author=request.POST.get('author')
        desc=request.POST.get('desc')
        pdf=request.FILES.get('pdf')
        Book(name=name,author=author,desc=desc,pdf=pdf).save()
        return redirect('librarian/librarianindex')

#class based view for editbook
class EditBook(UpdateView):
    model=Book
    fields=['name','author','desc','pdf']
    template_name="librarian/editbook.html"
    success_url =reverse_lazy('librarian/librarianindex')
    
#class based view for deleting a form field
'''class DeleteDataView(DeleteView):
    model=Book
    success_url = reverse_lazy('librarian/librarianindex')'''

#deleting data from form

def deletedata(request,id):
    data=Book.objects.get(id=id)
    data.delete()
    return redirect('librarian/librarianindex')
#Function based views for this project
'''def index(request):
    return render(request,"index.html")
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
    return render(request,'registration/register.html')'''
#librarian indexpage function based
'''@login_required
def librarianindex(request):
    data=Book.objects.all()
    return render(request,"librarian/librarianindex.html",{'obj':data})'''
#userindex page
'''@login_required
def userindex(request):
    data=Book.objects.all()
    return render(request,"user/userindex.html",{'obj':data})'''
    #userindexpage
'''def get(self,request):
        data=Book.objects.all()
        return render(request,"user/userindex.html",{'obj':data})'''
#for adding book

'''def addbook(request):
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
        return render(request,"librarian/addbook.html")'''
    
#editing form function based

'''def editbook(request, pk):
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
        return redirect('librarian/librarianindex')

    context = {'data':data}
    return render(request, 'librarian/editbook.html', context)'''