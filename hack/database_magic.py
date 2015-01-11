from .models import Class, Request, Session
from django.contrib.auth.models import User

def find_requests_class(class_name):
	solution = []
	C = Class.objects.filter(cid=class_name)
	R = Request.objects.filter(cls=C[0])
	print "GETTING THE REQUESTS"
	for request in R:
		solution.append(request.brit_dump())
	return solution


def create_session(people, time, length):
	S = Session(length=length, start=time)
	S.save()
	#emails()
	print "STARTING LOOP"
	for person in people.split(','):
		R = Request.objects.filter(id=int(person))
		#U = User.objects.filter(username=person)
		R.session = S
		print R
		R.save()
