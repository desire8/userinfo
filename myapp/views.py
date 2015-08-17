from django.shortcuts import render
from django.contrib.auth.models import User, Group
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from myapp.serializers import UserSerializer
from rest_framework import permissions

class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

def perform_create(self, serializer):
    serializer.save(owner=self.request.user)

@csrf_exempt
def user_list(request):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
   # nam3 = (request.user)
   # if str(nam3) == 'admin':

    if request.method == 'GET':
            users = User.objects.all()
            serializer = UserSerializer(users, many=True)

            return JSONResponse(serializer.data)

    elif request.method == 'POST':
            data = JSONParser().parse(request)
            username = (data['username'])

            User.objects.create(username=username)
            return JSONResponse("", status=201)
            #serializer = UserSerializer(data=data)
            #if serializer.is_valid():
            #    serializer.save()
            #    return JSONResponse(serializer.data, status=201)
            #return JSONResponse(serializer.errors, status=400)
    #else:
        #return JSONResponse("You are not admin", status=404)

@csrf_exempt
def user_detail(request, pk):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        users = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = UserSerializer(users)
        return JSONResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = UserSerializer(users, data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data)
        return JSONResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        users.delete()
        return HttpResponse(status=204)