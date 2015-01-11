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

def rest_view(request):
	if request.method == 'GET':
		dict = request.GET
	elif request.method == 'POST':
		dict = request.POST
	else:
		dict = {}
	
	action = dict.get( 'action' ) if 'action' in dict else ''
	if action == 'update':
		content = '[{"name":"CMPS 101"},{"name":"CMPS 104A"},{"name":"CMPS 111"},{"name":"CMPS 130","session":"blah"}]'
	else:
		content = '';
	response = HttpResponse( content_type = 'text/json' )
	response.content = content
	return response
