from .models import Class, Request

def find_requests_class(class_name):
	solution = []
	C = Class.objects.filter(cid=class_name)
	R = Request.objects.filter(cls=C[0])
	for request in R:
		solution.append(request.brit_dump())
	return solution