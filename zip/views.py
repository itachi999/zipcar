from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse

from . import user_views
from .models import Vehicle, Customer
from django.http import HttpResponse, HttpResponseRedirect
from . import urls
from .forms import *
import datetime
from dateutil.relativedelta import relativedelta

from django.shortcuts import render

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# from .forms import CarCreateForm
# CarSearchForm

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate


# Create your views here.

def default_view(request):
    return render(request, 'base.html')


def logout_request(request):
    logout(request)
    return HttpResponseRedirect('/')


def index(request):
    return render(request,'index.html')

@login_required
def special(request):
    return HttpResponse("You Just logged in, have an Awesome Experiance !")

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.last_membership_date=datetime.date.today()+ relativedelta(months=+6)
            profile.save()
            registered = True
            messages.success(request,'Welcome to ZipCar!! Please Log In to Rent a Vehicle.')
            return HttpResponseRedirect('/zip/login')
        else:
            print(user_form.errors,profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()
    return render(request,'registration/register.html',
                          {'user_form':user_form,
                           'profile_form':profile_form,
                           'registered':registered})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Your account was inactive.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details given")
    else:
        return render(request, 'registration/login.html', {})

# def extend_membership_view(request,u_id,extend_number):
#     # context={}
#     form=MembershipExtendForm()
#     user_object = User.objects.get(u_id)
#     customer = Customer.objects.get(user=user_object)
#     if request.method == 'POST' and form.is_valid():
#
#
#     context = {
#         'customer': customer
#     }
#     return render(request, 'zip/membership_details.html', context)


@login_required
def extend_membership_view(request):
    if not request.user.is_authenticated :
        return HttpResponseRedirect('/zip/login')
    form=MembershipExtendForm(request.POST or None)
    user = User.objects.get(username=request.user.username)
    customer = Customer.objects.get(user=user)
    context = {
        'customer': customer,
        'form': form,
    }
    if request.method == 'POST' and form.is_valid():
        number=form.cleaned_data['extend']
        if number=='extend1':
            customer.last_membership_date +=  relativedelta(months=+1)
        elif number=='extend3':
            customer.last_membership_date += relativedelta(months=+3)
        elif number=='extend6':
            customer.last_membership_date += relativedelta(months=+3)
        elif number == 'cancel':
            customer.last_membership_date = datetime.date.today()
        customer.save()
        HttpResponseRedirect('')

    return render(request,'zip/membership_details.html/',context)

def addmembership_view(request):
    # context={}
    print(request)
    return HttpResponse('okay')