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


'''   {% extends 'base.html' %}
{% block content %}
{% load static %}

<div class="container mt-5">
    {% if subscription.status == "active" %}
    <h4>Your subscription:</h4>
    <div class="card" style="width: 18rem;">
        <div class="card-body">
            <h5 class="card-title">{{ product.name }}</h5>
            <p class="card-text">
                {{ product.description }}
            </p>
            <button><a href="{% url 'user/pausesubscription' %}">Pause Subscription</a></button>
            <br>
            <br>
            <button><a href="{% url 'user/resumesubscription' %}">Resume Subscription</a></button>
            <br>
            <br>
            <button><a href="{% url 'user/updatesubscription' %}">Update Subscription</a></button>
            <br>
            <br>
            <button><a href="{% url 'user/accessmore' %}">See more</a></button>

        </div>
        {% endif %}
    </div>
</div>
<br>
<div class="container">

    {% if cancel_at_period_end %}
    <h4>Your membership will run to the end of your billing cycle.</h4>
    <br>
    <br>
    <button><a href="{% url 'user/userindexpage' %}">GO to Userindex page</a></button>
    <br>
    <br>
    {% elif membership %}
    <form action="{% url 'user/cancelsubscription' %}" method="POST">
        {% csrf_token %}
        <input type="submit" value="Cancel Membership?">
    </form>
    {% else %}
    <a href="{% url 'user/subscriptionplan' %}">Get a membership</a>
    {% endif %}
</div>
{% endblock %}'''