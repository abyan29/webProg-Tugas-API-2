from django.shortcuts import render
from django.http import JsonResponse
from myFirstapp.models import Course
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
import json,requests


@csrf_exempt
def apiCourse(request, course_id=None):
    if request.method == "GET":
        # Serialize the data into JSON        
        if course_id:
            course = Course.objects.get(pk=course_id)
            data = serializers.serialize("json", [course])
        else:
            data = serializers.serialize("json", Course.objects.all())
        # Turn the JSON data into a dict and send as JSON response             
        return JsonResponse(json.loads(data), safe=False)

    if request.method == "POST":
        # Turn the body into a dict        
        body = json.loads(request.body.decode("utf-8"))
        # Filter data        
        if not body:
            data = '{"message": "Data is not JSON type!"}'            
            dumps = json.loads(data)
            return JsonResponse(dumps, safe=False)
        else:
            created = Course.objects.create(course_name=body['course_name'])
            data = '{"message": "Data successfully created!"}'            
            dumps = json.loads(data)
            return JsonResponse(dumps, safe=False)

    if request.method == "PUT":
        if not course_id:
            return JsonResponse({'message': 'Course ID required'}, status=400)
        try:
            course = Course.objects.get(pk=course_id)
            body = json.loads(request.body.decode("utf-8"))
            if 'course_name' in body:
                course.course_name = body['course_name']
                course.save()
                return JsonResponse({'message': 'Course updated successfully'}, status=200)
            else:
                return JsonResponse({'message': 'Invalid data'}, status=400)
        except Course.DoesNotExist:
            return JsonResponse({'message': 'Course not found'}, status=404)

    if request.method == "DELETE":
        if not course_id:
            return JsonResponse({'message': 'Course ID required'}, status=400)
        try:
            course = Course.objects.get(pk=course_id)
            course.delete()
            return JsonResponse({'message': 'Course deleted successfully'}, status=204)
        except Course.DoesNotExist:
            return JsonResponse({'message': 'Course not found'}, status=404)

    return JsonResponse({'message': 'Method not allowed'}, status=405)

@csrf_exempt
def consumeApiGet (request):
    response = requests.get("https://jsonplaceholder.typicode.com/users")
    data = response.json()
    return render(request, "api-get.html",{'data': data})
