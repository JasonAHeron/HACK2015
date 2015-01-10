from django.shortcuts import render, render_to_response
from django.views.generic.base import TemplateView
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

class IndexView(TemplateView):
  template_name = 'index.html'

def test(request):
	return render_to_response('base.html', {'test': 1})

@csrf_exempt
def sms(request):
	twiml = '<Response><Message>Hey Study Student!</Message></Response>'
	return HttpResponse(twiml, content_type='text/xml')