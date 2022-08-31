import os
#import stripe
import stripe
from django.core.checks import messages
from django.contrib import messages
from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User,auth
from django.contrib.auth import logout
from .models import Book, Purchase,Customer
from django.contrib.auth.decorators import login_required
from django.conf import settings
from.form import EditForm
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views import View
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView

stripe.api_key = settings.STRIPE_SECRET_KEY

# Create your views here.
#for loading homepage
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
            #send_mail('Login successful','Welcome to our mini bookstore!!',\
            # settings.EMAIL_HOST_USER,[username])
            #request.session['AUTHSESSION']=username
            return redirect('user/userindexpage')
        else:
            messages.info(request, 'invalid credentials')
            return redirect('registration/loginpage')

#class based view for registration
class RegisterView(View):
    def get(self,request):
        return render(request,"registration/register.html")

    def post(self,request):
        username=request.POST['username']
        password=request.POST['password']
        #confirm password
        password2=request.POST['password2'] 
        if password==password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'username already taken')
                return redirect('registration/loginpage')
            else:
                user=User.objects.create_user(username=username,password=password)
                user.save()
                #send_mail('Registration successful',\
                # 'Login to see more!!',settings.EMAIL_HOST_USER,[username])
                return redirect('registration/loginpage')
        else:
            messages.info(request, 'password is not matching...')
            return redirect('registration/registerpage')

#class based view for viewing index page
class LibrarianIndexView(ListView):
    model=Book
    template_name="librarian/librarianindex.html"
    context_object_name='obj'

#class based view for userindexpage
class UserIndexView(ListView):
    model=Book
    paginate_by = 3
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

class DeleteDataView(View):
    def get(self,request,pk):
        return render(request,"librarian/book_confirm_delete.html")

    def post(self,request,pk):
        data=Book.objects.get(id=pk)
        data.delete()
        return redirect('librarian/librarianindex')

#logout
class LogoutView(View):
    def get(self, request):
        logout(request)
        return render(request,"index.html")


#stripe onetime payment implementation

@login_required
def checkout(request):
    final_dollar = 600
    price_id='price_1KyU5ZSGnrdrktnN36LDP8RB'
    session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            customer_email=request.user.username,
            line_items=[{
                'price': price_id,
                'quantity': 1,
            }],
            mode='payment',
            allow_promotion_codes=True,
            success_url='http://127.0.0.1:8000/success?session_id={CHECKOUT_SESSION_ID}',
            cancel_url='http://127.0.0.1:8000/cancel',
    )

    return render(request, 'user/checkout.html', {'final_dollar': final_dollar,\
         'session_id': session.id})

def success(request):
    return render(request, 'user/success.html')

def cancel(request):
    return render(request, 'user/cancel.html')

#subscription implementation

#creating a checkout for subscription

@login_required
def checkoutsubscription(request):

    try:
        if request.user.customer.membership:
            return redirect('user/userindex')
    except Customer.DoesNotExist:
        pass

    if request.method == 'POST':
        pass
    else:
        membership = 'monthly'
        final_dollar = 300
        membership_id = 'price_1KzvGQSGnrdrktnNasRrJk4g'
        if request.method == 'GET' and 'membership' in request.GET:
            if request.GET['membership'] == 'yearly':
                membership = 'yearly'
                membership_id = 'price_1KzvGxSGnrdrktnNPVv4aX6f'
                final_dollar = 800

        # Create Stripe Checkout
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            customer_email=request.user.username,
            line_items=[{
                'price': membership_id,
                'quantity': 1,
            }],
            mode='subscription',
            #allow_promotion_codes=True,
            success_url='http://127.0.0.1:8000/successsub?session_id={CHECKOUT_SESSION_ID}',
            cancel_url='http://127.0.0.1:8000/cancel',
        )

        return render(request, 'user/checkoutsubscription.html', {'final_dollar': final_dollar, 'session_id': session.id})
    
#after successfull subscription

def successsubscription(request):
    if request.method == 'GET' and 'session_id' in request.GET:
        session = stripe.checkout.Session.retrieve(request.GET['session_id'],)
        customer = Customer()
        customer.user = request.user
        customer.stripeid = session.customer
        customer.membership = True
        customer.cancel_at_period_end = False
        customer.stripe_subscription_id = session.subscription
        customer.save()
        subscription = stripe.Subscription.retrieve(
            customer.stripe_subscription_id)
        product = stripe.Product.retrieve(subscription.plan.product)
    return render(request, 'user/subscriptionsuccess.html', {'subscription': subscription, 'product': product})

#subscription plan (monthly or yearly)
def joinplan(request):
    return render(request, 'user/subscriptionplan.html')

#cancel subscription
@login_required
def cancelsubscription(request):
    membership = False
    cancel_at_period_end = False
    if request.method == 'POST':
        subscription = stripe.Subscription.retrieve(
            request.user.customer.stripe_subscription_id)
        subscription.cancel_at_period_end = True
        request.user.customer.cancel_at_period_end = True
        cancel_at_period_end = True
        subscription.save()
        request.user.customer.save()
    else:
        try:
            if request.user.customer.membership:
                membership = True
                subscription = stripe.Subscription.retrieve(
                    request.user.customer.stripe_subscription_id)
                #product = stripe.Product.retrieve(subscription.plan.product)
            if request.user.customer.cancel_at_period_end:
                cancel_at_period_end = True
        except Customer.DoesNotExist:
            membership = False
    return render(request, 'user/cancelsubscription.html', {'membership': membership, 'cancel_at_period_end': cancel_at_period_end})



#pause a subscription
def pausesubscription(request):
    cid = stripe.Subscription.retrieve(
        request.user.customer.stripe_subscription_id),
    stripe.Subscription.modify(
        request.user.customer.stripe_subscription_id,
        pause_collection={
            'behavior': 'mark_uncollectible',
        },
    )
    # return HttpResponse("Successfully paused")
    return render(request, 'user/pause.html')

#resume a subscription
def resumesubscription(request):
    cid = stripe.Subscription.retrieve(
        request.user.customer.stripe_subscription_id),
    stripe.Subscription.modify(
        request.user.customer.stripe_subscription_id,
        pause_collection='',
    )
    # return HttpResponse("Resumed")
    return render(request, 'user/resume.html')

#update a subscription

def updatesubscription(request):
    if request.method == 'GET':
        subscription =  stripe.Subscription.retrieve(request.user.customer.stripe_subscription_id)
        stripe.Subscription.modify(
        subscription.id,
        cancel_at_period_end=False,
        proration_behavior='create_prorations',
        items=[{
            'id': subscription['items']['data'][0].id,
            
            'price': 'price_1KzvGxSGnrdrktnNPVv4aX6f',
            
            
        }]
        )
        
        return render(request,'user/update.html')

#only subscribed users can see this page

def accessmore(request):
    return render(request,'user/accessmore.html')


