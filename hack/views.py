from django.shortcuts import render, render_to_response
from django.views.generic.base import TemplateView

class IndexView(TemplateView):
  template_name = 'index.html'

def test(request):
	return render_to_response('base.html', {'test': 1})