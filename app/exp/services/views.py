from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import urllib.request
import urllib.parse
import json

def show_all_users(request):
    req = urllib.request.Request('http://models:8000/api/v1/user/')
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)
    print(resp)
    return JsonResponse(resp, safe=False)

def user_detail(request, uid):
    url = 'http://models:8000/api/v1/user/' + str(uid) + "/"
    req = urllib.request.Request(url)
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)
    print(resp)
    return JsonResponse(resp, safe=False)
