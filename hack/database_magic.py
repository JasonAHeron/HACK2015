from .models import Class, Request

def find_requests_class(class_name):
	C = Class.objects.filter(cid=class_name)
	R = Request.objects.filter(cls=C[0])
	for request in R:
		print request.brit_dump()