from django.shortcuts import render, render_to_response
from django.views.generic.base import TemplateView
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from hack.forms import UserForm, UserProfileForm
from django.template import RequestContext
from django.contrib.auth import authenticate, login
from .models import Class, Request, UserProfile, Schedule
from .build_classes import scrape_classes
from django.contrib.auth.views import logout
import json
from .database_magic import find_requests_class, create_session

#email 
import threading
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags

#new imports, twil update 
from django_twilio.decorators import twilio_view
from twilio.twiml import Response
from twilio.rest import TwilioRestClient

#algorithm
import ast
import re

def create_schedule(list_of_users):
#    newguy_avail_list = [5,9,12,14]
    newguy_locations = [1,2,3]

    strings = []
    i = 0
    index_start = 0

    #get data for the cid. as a list of dictionaries.

    print "GIVEN:"
    print list_of_users
    print "OLD USERS:"
    old_guys = list_of_users[:len(list_of_users)-1]
    print old_guys
    print "NEW GUY:"
    new_guy = list_of_users[len(list_of_users)-1]
    new_guy_schedule = new_guy["schedule"]
    print new_guy
    newguy_min_time = new_guy["minT"]*2 #convert half hrs to hours
    newguy_people = new_guy["minP"]

    #convert string to a dictionary
    #yoyo_d = ast.literal_eval(yoyo)
    days_of_week = []
    for i in range(7):
        days_of_week.append([])
    for persons_dictionary in old_guys:
        
        persons_availability_dict = persons_dictionary['schedule']
        d = 0
        for day in persons_availability_dict:

            avail_times_of_day = days_of_week[d]
            d += 1
            for i in range(100 + 1):
                avail_times_of_day.append("")
            start = 0
            time_tuples = persons_availability_dict[day]

            while(len(time_tuples) >= start+2):
                if(time_tuples[start+1] - time_tuples[start] >= newguy_min_time):
                    print " diff was using " + str(time_tuples[start+1]) +  ",  " +  str(time_tuples[start])
                    #print persons_dictionary['id']
                    #print "START!!!"
                    #print time_tuples[start]
                    
                    #heart of the algorithm
                    avail_times_of_day[time_tuples[start]] += persons_dictionary['id'] + ","
                start += 2

    newguy_itor = 0
    
    #this is a list of lists
    newguy_days_of_week = []
    for i in range(7):
        newguy_days_of_week.append([])
    for i in range(7):
        newguy_days_of_week[i] = []
    # guy needs to meet his own needs
    new_d = -1
    #day is a list itself
    for day in new_guy_schedule:
        new_d += 1
        newguy_avail_list = new_guy_schedule[day]
        if (len(newguy_days_of_week) > new_d):
            print "DAY !!!!!"
            print day
            while(len(newguy_avail_list) >= newguy_itor+2):
                print "IN WHILE LOOP"
                if(newguy_avail_list[newguy_itor+1] - newguy_avail_list[newguy_itor] >= newguy_min_time):
                    print "IN IF STMT"
                    print "LEN IS"
                    print len(newguy_days_of_week)
                    print "new_d is"
                    print new_d
                    if (len(newguy_days_of_week)-1 >= new_d):
                        #print newguy_days_of_week[new_d]
                        print "test"
                        newguy_days_of_week[new_d].append(newguy_avail_list[newguy_itor])
                    #print newguy_days_of_week[new_d]
                    #print new_d
                    #print "start time here: " 
                    #print newguy_avail_list[newguy_itor]
                newguy_itor+=2

    print "OUT OF LOOP"
    print newguy_days_of_week
    curr_day = -1
    for old_guy_day in days_of_week:
        curr_day += 1
        #look through all the avail times of newguy
        print "NEW GUY TIMES FOR CURR DAY"
        print newguy_days_of_week[curr_day]
        if (len(newguy_days_of_week) > curr_day):
           for newg_start_time in newguy_days_of_week[curr_day]:
               #if that index in the old_guy_day is not empty
               print "ARRAY WE ARE WORKING WITH"
               print old_guy_day[newg_start_time]
               #check that the length after .split is atleast min
               if(len(old_guy_day[newg_start_time].split(",")) >= newguy_min_time):
                   #save the match (print it for now)
                   print "THIS START TIME WORKS IN BOTH:"
                   print newg_start_time
                   print "HERE ARE THE FRIENDS:"
                   print old_guy_day[newg_start_time]
                   new_list = old_guy_day[newg_start_time] + new_guy['id']
                   create_session(new_list, newg_start_time, newguy_min_time)
                   return None

    print "END OF FUNCITON"

def index_view(request):
    context = RequestContext(request)
    current_user = request.user

    if current_user.is_active:
        S = Schedule.objects.filter(user=current_user)
        if len(S) > 0:
            schedule = json.loads(S[0].schedule)
        else:
            schedule = [[],[],[],[],[],[],[]]
    else:
        schedule = [[],[],[],[],[],[],[]]
    if request.POST.get('signin'):
        print "THE CONDITION WAS ACCEPTED"
        user = authenticate (username=request.POST.get('username') , password=request.POST.get('password'))
        if not user or not user.is_active:
            print "Sorry, that login was invalid. Please try again."
            return render_to_response('issues.html', {'username': request.POST.get('username'), 'password':request.POST.get('password')}, context)
        else:
            login(request, user)
    if request.POST.get('logout'):
        print "TRYING TO LOGOUT"
        logout(request)
        return HttpResponseRedirect("")

    solution = []
    for c_object in Class.objects.all():
        solution.append("{}".format(c_object.cid))
    return render_to_response('index.html', {'classes': solution, 'schedule': schedule}, context)

def issues(request):
    return render_to_response('index.html', context)

def test(request):
    return render_to_response('base.html', {'test': 1})

@twilio_view
def sms(request):
    name = request.POST.get('Body', '')
    msg = 'Hey %s, how are you today?' % (name)
    r = Response()
    r.message(name)
    return r

def send_message():
    # Your Account Sid and Auth Token from twilio.com/user/account
    account_sid = "ACe5e1624beb9d42623af561bdc50544dc"
    auth_token  = "d6fe80ae0da4aea45bed7c47e5a5dfc3"
    client = TwilioRestClient(account_sid, auth_token)
 
    d = {'brittany':"+16508687814", 'jason':"+13109917156"}
    for key, value in d.iteritems():
        message = client.messages.create(body="Hey %s. You are signed up for a study group!" % (key),
            to = value, 
            from_="+16503999494")
        print message.sid

def rest_view(request):
    current_user = request.user
    profile = current_user.get_profile()
    phone = profile.phone

    if request.method == 'GET':
        dict = request.GET
    elif request.method == 'POST':
        dict = request.POST
    else:
        dict = {}
    	
    action = dict.get( 'action' ) if 'action' in dict else ''
    if action == 'create':
        dct = json.loads(request.POST.get('data'))
        cid = dct.get('class')
        people = dct.get('minUsers')
        schedule = str(dct.get('schedule'))
        time = dct.get('minTime')
        class_ = Class.objects.filter(cid=cid)
        print "PHONE NUMER {}".format(phone)
        R = Request(phone=phone, schedule=schedule, cls=class_[0], user=current_user, time=time, people=people)
        R.save()

        #brit, sara querry
        create_schedule(find_requests_class(cid))




    if action == 'schedule':
        dct = json.loads(dict.get('data'))
        if Schedule.objects.filter(user=current_user).exists():
            Schedule.objects.filter(user=current_user).delete()
        S = Schedule(user=current_user, schedule=dct).save()

        '''
    elif action == 'email':
        print dict['data']
    elif action == 'password':
        print dict['data']
    elif action == 'phoneNumber':
        print dict['data']
        '''

    if action == 'update':
        requests = Request.objects.filter(user=current_user.id)
        sol = []
        for request in requests:
            dict = {}
            dict['name'] = request.cls.cid
            sol.append(dict)
        content = json.dumps(sol)
    else:
        content = '';
    response = HttpResponse(content_type = 'text/json')
    response.content = content
    return response
	
def register(request):
    # Like before, get the request's context.
    context = RequestContext(request)

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    #get all of the fields that the user typed in
    print "REGISTER VIEW CALLED"
    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        print "REGISTER POST CALLED"
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.

        #these are the ones we added on top of default reg for django
        #phone = request.POST.get('phone')
        #firstname = request.POST.get('firstname')
        #lastname = request.POST.get('lastname')

        user_form = UserForm(data=request.POST)
        print request.POST
        profile_form = UserProfileForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()
            print "NEW USER IN THE MAKING"
            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user

            # PUT IN LOGIC FOR THE BOOLEANS AND THE PHONE NUMBER
            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and put it in the UserProfile model.
            # if 'picture' in request.FILES:
            #    profile.picture = request.FILES['picture']

            # Now we save the UserProfile model instance.
            profile.save()

            # Update our variable to tell the template registration was successful.
            registered = True

            user = authenticate (username=request.POST['username'], password=request.POST['password'])
            login(request, user)
            send_email(request.POST['username'], request.POST['first_name'])
            #thread1.start()
            return HttpResponseRedirect('/')

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print "THERE WAS AN ERROR"
            print user_form.errors, profile_form.errors
        render_to_response('register.html', context)

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

        # Render the template depending on the context.
        return render_to_response(
            'register.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered},
            context)
    #r = Response()
    #r.message('Hello from your Django app!')
    #return r

def send_email(sendtoemail, firstname):
    subject = 'Welcome Banana Slug to Your UCSC Study Group Scheduler!'
    from_email = 'learnallthethings1@gmail.com'
    html_content = render_to_string('email.html', {'varname':'value', 'first_name':firstname})
    text_content = strip_tags(html_content) 
    msg = EmailMultiAlternatives(subject, text_content, from_email, [sendtoemail])
    msg.attach_alternative(html_content, "text/html")
    msg.send() #make this on another threading

def send_session_email(sendtoemail, day, starthour):
    subject = 'You have just been added to a new UCSC Study Session!'
    from_email = 'learnallthethings1@gmail.com'
    html_content = render_to_string('emailSession.html', {'varname':'value', 'studyday':day, 'starthour':starthour})
    text_content = strip_tags(html_content) 
    msg = EmailMultiAlternatives(subject, text_content, from_email, [sendtoemail])
    msg.attach_alternative(html_content, "text/html")
    msg.send() #make this on another threading

def build_classes(request):
    classes = scrape_classes()
    for class_ in classes:
        Class(cid=class_).save()
    return render_to_response('build.html', {'classes': Class.objects.all()})
