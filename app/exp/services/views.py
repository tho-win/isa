from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from urllib.error import URLError, HTTPError
import urllib.request
import urllib.parse
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password, check_password
import os
import hmac
from django.conf import settings
from kafka import KafkaProducer
from elasticsearch import Elasticsearch

producer = KafkaProducer(bootstrap_servers='kafka:9092')

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
    for p in resp:
        seller = get_user_by_username(p['seller'])
        p['seller'] = seller

    return JsonResponse(resp, safe=False)

def show_all_authenticators(request):
    req = urllib.request.Request('http://models:8000/api/v1/authenticator/')
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)
    print(resp)
    return JsonResponse(resp, safe=False)

def user_detail(request, uid):
    url = 'http://models:8000/api/v1/user/' + str(uid) + "/"
    req = urllib.request.Request(url)
    try:
        response = urllib.request.urlopen(req)
    except urllib.error.URLError as e:
        err_resp = {"error status" : e.code, "error reason": e.reason}
        return JsonResponse(err_resp, safe=False)
    resp_json = response.read().decode('utf-8')
    resp = json.loads(resp_json)
    return JsonResponse(resp, safe=False)

def get_user_by_username(username):
    url = 'http://models:8000/api/v1/user/?username=' + username
    req = urllib.request.Request(url)
    try:
        resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    except HTTPError as e:
        return None
    resp = json.loads(resp_json)
    return resp

def post_detail(request, pid):
    resp = get_post_by_id(pid)
    data = {'id' : pid}
    producer.send('listing-view-topic', json.dumps(data).encode('utf-8'))
    return JsonResponse(resp, safe=False)
    

def get_post_by_id(pid):
    url = 'http://models:8000/api/v1/post/' + str(pid) + "/"
    req = urllib.request.Request(url)
    try:
        response = urllib.request.urlopen(req)
    except urllib.error.URLError as e:
        err_resp = {'ok': False, "error status" : e.code, "error reason": e.reason}
        return err_resp
    resp_json = response.read().decode('utf-8')
    resp = json.loads(resp_json)
    seller_url = resp['seller']
    resp['seller'] = get_user_by_username(seller_url)
    resp['ok'] = True
    return resp

# def retrieve_user(request, uid):
#     url = 'http://models:8000/api/v1/get_user/' + str(uid) + "/"
#     req = urllib.request.Request(url)
#     resp_json = urllib.request.urlopen(req).read().decode('utf-8')
#     resp = json.loads(resp_json)
#     print(resp)
#     return JsonResponse(resp, safe=False)


'''
err_code: 
    0 : username does not exist
    1 : username exists but the password does not match
    2 : email already exists
    3 : username already exists
    4 : unknown failure
'''

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
        try: 
            response = urllib.request.urlopen(req)
        except urllib.error.URLError as e:
            get_url = 'http://models:8000/api/v1/user/?username=' + request.POST.get('username')
            get_req = urllib.request.Request(get_url)
            get_resp_json = urllib.request.urlopen(get_req).read().decode('utf-8')
            get_resp = json.loads(get_resp_json)
            if (len(get_resp) > 0):
                return JsonResponse({'ok': False, "err_code": 3}, safe=False)
            else:
                return JsonResponse({'ok': False, "err_code": 2}, safe=False) 

        resp_json = response.read().decode('utf-8')
        resp = json.loads(resp_json)
        return JsonResponse({'ok': True, 'username': request.POST.get('username'), 'password': request.POST.get('password'),
                              'email': request.POST.get('email')}, safe=False)   
    else: 
        return JsonResponse([{'return': 'for not post'}], safe=False)


@csrf_exempt
def create_listing(request):
    if request.method == 'POST':
        data = {}
        data['seller'] = request.POST.get('seller')
        data['seller_id'] = request.POST.get('seller_id')
        data['title'] = request.POST.get('title')
        data['content'] = request.POST.get('content')
        data['price'] = request.POST.get('price')
        data['remaining_nums'] = request.POST.get('remaining_nums')
        data['pickup_address'] = request.POST.get('pickup_address')
        raw_data = data
        data = urllib.parse.urlencode(data).encode()

        req = urllib.request.Request('http://models:8000/api/v1/post/', data=data)
        try:
            response = urllib.request.urlopen(req)
        except urllib.error.URLError as e:
            return JsonResponse([{'ok': False, 'code': e.code, 'reason': e.reason, 'data': str(raw_data)}], safe=False) 

        resp_json = response.read().decode('utf-8')
        resp = json.loads(resp_json)
        queue_listing(resp)
        return JsonResponse([{'ok': True, 'resp': str(resp)}], safe=False) 
    else: 
        return JsonResponse([{'result': 'not post'}], safe=False)

def queue_listing(listing):
    #producer = KafkaProducer(bootstrap_servers='kafka:9092')
    #listing.pop('seller')
    listing.pop('url')
    new_listing = listing
    producer.send('new-listings-topic', json.dumps(new_listing).encode('utf-8'))


@csrf_exempt
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        url = 'http://models:8000/api/v1/user/?username=' + username
        req = urllib.request.Request(url)
        try:
            response = urllib.request.urlopen(req)
        # unknown bad request
        except urllib.error.URLError as e:
            resp = {'ok': False, 'err_code': 4}
            return JsonResponse(resp, safe=False)

        resp_json = response.read().decode('utf-8')
        resp = json.loads(resp_json)
        # cannot find the username
        if (len(resp) == 0):
            resp = {'ok': False, "err_code": 0}
            return JsonResponse(resp, safe=False)
        encodedPassword = resp[0]['password']
        first_name = resp[0]['first_name']
        user_id = resp[0]['id']
        if check_password(password, encodedPassword):
            user_id = resp[0]['id']
            authenticator = create_authenticator(user_id)
            resp = {'ok': True, 'authenticator': authenticator, 'first_name': first_name, 'user_id': user_id}
            return JsonResponse(resp, safe=False)
        # username and password don't match
        else:
            resp = {'ok': False, "err_code": 1}
            return JsonResponse(resp, safe=False)
        
    else: 
        return JsonResponse({'result': 'not post'}, safe=False)


@csrf_exempt
def profile_update(request):
    if request.method == 'POST':
        data = request.POST
        data = urllib.parse.urlencode(data).encode()
        url = 'http://models:8000/api/v1/user/' + str(request.POST.get("id")) + "/"
        req = urllib.request.Request(url=url, data=data, method='PATCH')
        try: 
            response = urllib.request.urlopen(req)
        except urllib.error.URLError as e:
            get_url = 'http://models:8000/api/v1/user/?username=' + request.POST.get('username')
            get_req = urllib.request.Request(get_url)
            get_resp_json = urllib.request.urlopen(get_req).read().decode('utf-8')
            get_resp = json.loads(get_resp_json)
            if (len(get_resp) > 0):
                return JsonResponse({'ok': False, "err_code": 3}, safe=False)
            else:
                return JsonResponse({'ok': False, "err_code": 2}, safe=False) 
        return JsonResponse({'ok': True}, safe=False) 
    else:
        return JsonResponse({'ok': False, 'result': 'not post'}, safe=False)


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
            return JsonResponse({'ok': 0}, safe=False)
        return JsonResponse({'ok': 1}, safe=False)
    else: return JsonResponse({'GET request': 'invalid'}, safe=False)


@csrf_exempt
def delete_auth(request, auth):
    #find that auth in db
    url = 'http://models:8000/api/v1/authenticator/?authenticator=' + auth
    req = urllib.request.Request(url)
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)
    if len(resp) > 0:
        auth_id = resp[0]['id']
    url = 'http://models:8000/api/v1/authenticator/' + str(auth_id) + '/'
    req = urllib.request.Request(url, method='DELETE')
    try:
        resp_json = urllib.request.urlopen(req).read().decode('utf-8')
        return JsonResponse({'deleted?': True}, safe=False)
    except URLError as e:
        return JsonResponse({'error': 'Cannot delete auth'}, safe=False)
        


@csrf_exempt
def search_listing(request):
    if request.method == 'POST':
        query = request.POST.get('query')
        es = Elasticsearch(['es'])
        # recall = es.search(index='listing_index', body={'query': {'query_string': {'query': query}}, 'size': 10})
        recall = es.search(index='listing_index', body={"query": {"function_score": {"query": {"query_string": {"query": query}},
            "field_value_factor": {"field": "visits","modifier": "log1p","missing": 0.1}}}})
        raw_recall = recall
        if recall['hits']['total']['value'] == 0:
            return JsonResponse({'ok': False})
        else:
            recall = process_recall(recall['hits'])
            ret = {'ok': True, 'result': recall, 'raw_recall': str(raw_recall['hits']['hits'])}
            return JsonResponse(ret, safe=False)
    else: return JsonResponse({'return': 'not post'}, safe=False)

    
def process_recall(recall):
    ret = []
    for item in recall['hits']:
        listing_score = {}
        listing_id = item['_source']['id']
        listing = get_post_by_id(listing_id)
        listing_score["listing"] = listing
        listing_score["score"] = item['_score']
        ret.append(listing_score)
    return ret


