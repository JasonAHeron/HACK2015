from django.shortcuts import render, render_to_response
from django.views.generic.base import TemplateView
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from hack.forms import UserForm, UserProfileForm
from django.template import RequestContext
from django.contrib.auth import authenticate, login
from .models import Class, Request
from .build_classes import scrape_classes
from django.contrib.auth.views import logout
import json

#new imports, twil update 
from django_twilio.decorators import twilio_view
from twilio.twiml import Response
from twilio.rest import TwilioRestClient

def index_view(request):
    context = RequestContext(request)
    current_user = request.user
    if request.POST.get('approveSchedule'):
        cid = request.POST.get('class')
        people = request.POST.get('people')
        gender = request.POST.get('gender')
        time = request.POST.get('time')
        class_ = Class.objects.filter(cid=cid)
        Request(cls=class_[0], user=current_user, time=time, people=people).save()

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
    return render_to_response('index.html', {'classes': solution}, context)

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

	if request.method == 'GET':
		dict = request.GET
	elif request.method == 'POST':
		dict = request.POST
	else:
		dict = {}
	
	action = dict.get( 'action' ) if 'action' in dict else ''
	if action == 'update':
	#	requests = Request.objects.filter(user=current_user.id)
	#	sol = []
	#	for request in requests:
	#		dict = {}
	#		dict['name'] = request.cls.cid
	#		sol.append(dict)
	#	content = json.dumps(sol)
		content = '[{"name":"CMPS 101"}, {"name":"CMPS 130", "session":"blah"}]'
	else:
		content = '';
	response = HttpResponse(content_type = 'text/json')
	response.content = content
	return response
	
def register(request):
    # Like before, get the request's context.
    #send_message() /// this sends text messages to people in the dict in this function
    context = RequestContext(request)

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    #get all of the fields that the user typed in

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
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

def build_classes(request):
	classes = scrape_classes()
	for class_ in classes:
		Class(cid=class_).save()
	return render_to_response('build.html', {'classes': Class.objects.all()})
