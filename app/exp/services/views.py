from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import urllib.request
import urllib.parse
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password, check_password
import os
import hmac
from django.conf import settings

def show_all_users(request):
    req = urllib.request.Request('http://models:8000/api/v1/user/')
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)
    print(resp)
    return JsonResponse(resp, safe=False)


def show_all_posts(request):
    req = urllib.request.Request('http://models:8000/api/v1/post/')
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

def post_detail(request, pid):
    url = 'http://models:8000/api/v1/post/' + str(pid) + "/"
    req = urllib.request.Request(url)
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)
    print(resp)
    return JsonResponse(resp, safe=False)

@csrf_exempt
def create_user(request):
    if request.method == 'POST':
        data = {}
        #'username', 'password', 'email', 'first_name', 'last_name', 'computing_id', 'phone_number', 'bio'
        data['username'] = request.POST.get('username')
        data['password'] = make_password(request.POST.get('password'))
        data['email'] = request.POST.get('email')
        data['first_name'] = request.POST.get('first_name')
        data['last_name'] = request.POST.get('last_name')
        data['computing_id'] = request.POST.get('computing_id')
        data['phone_number'] = request.POST.get('phone_number')
        data['bio'] = request.POST.get('bio')
        
        data = urllib.parse.urlencode(data).encode()
        req = urllib.request.Request('http://models:8000/api/v1/user/', data=data)
        resp_json = urllib.request.urlopen(req).read().decode('utf-8')
        ###need to check resp_json is valid
        resp = json.loads(resp_json)
        return JsonResponse([{'username': request.POST.get('username'), 'password': request.POST.get('password')}], safe=False)
        
    else: return JsonResponse([{'return': 'for not post'}], safe=False)

@csrf_exempt
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        url = 'http://models:8000/api/v1/user/?username=' + username
        req = urllib.request.Request(url)
        resp_json = urllib.request.urlopen(req).read().decode('utf-8')
        resp = json.loads(resp_json)
        encodedPassword = resp[0]['password']
        first_name = resp[0]['first_name']
        if check_password(password, encodedPassword):
            user_id = resp[0]['id']
            authenticator = create_authenticator(user_id)
            resp = [{'ok': True, 'authenticator': authenticator, 'first_name': first_name}]
            return JsonResponse(resp, safe=False)
        
    else: return JsonResponse([{'result': 'no post'}], safe=False)

def create_authenticator(user_id):
    authenticator = hmac.new(
        key = settings.SECRET_KEY.encode('utf-8'),
        msg = os.urandom(32),
        digestmod = 'sha256',
    ).hexdigest()
    data = {'authenticator': authenticator, 'user_id': user_id}
    data = urllib.parse.urlencode(data).encode()
    req = urllib.request.Request('http://models:8000/api/v1/authenticator/', data=data)
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)
    return resp['authenticator']

@csrf_exempt
def check_auth(request):
    if request.method == 'POST':
        auth = request.POST.get('authenticator')
        url = 'http://models:8000/api/v1/authenticator/?authenticator=' + auth
        req = urllib.request.Request(url)
        resp_json = urllib.request.urlopen(req).read().decode('utf-8')
        resp = json.loads(resp_json)
        if len(resp) == 0:
            return JsonResponse([{'ok': 0}], safe=False)
        return JsonResponse([{'ok': 1}], safe=False)
    else: return JsonResponse([{'GET request': 'invalid'}], safe=False)