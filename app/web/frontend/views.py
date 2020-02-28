from django.shortcuts import render, render_to_response
from django.http import HttpResponse, JsonResponse
import urllib.request
import urllib.parse
import json

# Create your views here.

def homepage(request):
    return render(request, 'frontend/homepage.html')

def show_all_users(request):
    req = urllib.request.Request('http://exp:8000/users/')
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)
    users = {}
    for u in resp:
        users[u['username']] = u
    context = {"test key": "test value"}
    return render(request, "frontend/users.html", {'users': users})
    #return JsonResponse(users, safe=False)
    #return HttpResponse("user")

def user_detail(request, uid):
    url = 'http://exp:8000/users/' + str(uid) + "/"
    req = urllib.request.Request(url)
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)
    return render(request, "frontend/user_detail.html", {'user': resp})