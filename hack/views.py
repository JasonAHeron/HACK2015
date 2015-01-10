from django.shortcuts import render, render_to_response
from django.views.generic.base import TemplateView
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

#new imports, twil update
from django_twilio.decorators import twilio_view
from twilio.twiml import Response

class IndexView(TemplateView):
  template_name = 'index.html'

def test(request):
	return render_to_response('base.html', {'test': 1})

@twilio_view
def sms(request):
	r = Response()
	r.message('Hello from your Django app!')
	return r