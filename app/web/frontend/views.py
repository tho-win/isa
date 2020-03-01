from django.shortcuts import render, render_to_response
from django.http import HttpResponse, JsonResponse
import urllib.request
import urllib.parse
import datetime
import json


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
    return render(request, "frontend/all_users.html", {'users': users})
   

def user_detail(request, uid):
    url = 'http://exp:8000/users/' + str(uid) + "/"
    req = urllib.request.Request(url)
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)
    return render(request, "frontend/user_detail.html", {'user': resp})


def show_all_posts(request):
    all_posts_req = urllib.request.Request('http://exp:8000/posts/')
    all_posts_resp_json = urllib.request.urlopen(all_posts_req).read().decode('utf-8')
    all_posts_resp = json.loads(all_posts_resp_json)

    return render(request, 'frontend/all_posts.html', {"posts" : all_posts_resp})


def show_special_posts(request):
    all_posts_req = urllib.request.Request('http://exp:8000/posts/')
    all_posts_resp_json = urllib.request.urlopen(all_posts_req).read().decode('utf-8')
    all_posts_resp = json.loads(all_posts_resp_json)

    # get latest post
    latest_post = all_posts_resp[0]
    # get cheapest post and get post with most swipes
    min_price, min_price_index = all_posts_resp[0]["price"], 0
    max_swipe, max_swipe_index = all_posts_resp[0]["remaining_nums"], 0
    for i in range(len(all_posts_resp)):
        post = all_posts_resp[i]
        if (post["price"] < min_price):
            min_price = post["price"]
            min_price_index = i
        if (post["remaining_nums"] > max_swipe):
            max_swipe = post["remaining_nums"]
            max_swipe_index = i
    cheapest_post = all_posts_resp[min_price_index]
    most_swipe_post = all_posts_resp[max_swipe_index]

    return render(request, 'frontend/special_posts.html', {'latest_post' : latest_post, 
                                                "cheapest_post" : cheapest_post, "most_swipe_post" : most_swipe_post})
