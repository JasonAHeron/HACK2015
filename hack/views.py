from django.shortcuts import render, render_to_response
from django.views.generic.base import TemplateView
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from hack.forms import UserForm, UserProfileForm
from django.template import RequestContext
from django.contrib.auth import authenticate, login

from .models import Class
from .build_classes import scrape_classes

#new imports, twil update 
from django_twilio.decorators import twilio_view
from twilio.twiml import Response

def index_view(request):
	return render_to_response('index.html', {'classes': Class.objects.all()})

def test(request):
	return render_to_response('base.html', {'test': 1})

@twilio_view
def sms(request):

	twiml = '<Response><Message>Hey Study Student!</Message></Response>'
	return HttpResponse(twiml, content_type='text/xml')

def register(request):
    # Like before, get the request's context.
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

