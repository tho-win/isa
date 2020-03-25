from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from urllib.error import URLError, HTTPError
from frontend.forms import SignUpForm, LogInForm, CreatePostForm
from django.shortcuts import render, render_to_response
from django.views.generic import TemplateView
from .models import DummyUser
from django.contrib import messages
from django.urls import reverse
import urllib.request
import urllib.parse
import datetime
import json


def homepage(request):
    all_posts_req = urllib.request.Request('http://exp:8000/posts/')
    all_posts_resp_json = urllib.request.urlopen(all_posts_req).read().decode('utf-8')
    all_posts_resp = json.loads(all_posts_resp_json)
    auth = request.COOKIES.get('auth')
    if auth:
        if check_auth(auth):
            return render(request, 'frontend/homepage.html', {'posts': all_posts_resp})

    return render(request, 'frontend/homepage.html', {'posts': all_posts_resp})

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
    if (resp['ok']):
        return render(request, "frontend/user_detail.html", {'user': resp})
    else: 
        err_msg = "Sorry! This user doesn't exist."
        return render(request, "frontend/user_detail.html", {'err_msg': err_msg})


def show_all_posts(request):
    all_posts_req = urllib.request.Request('http://exp:8000/posts/')
    all_posts_resp_json = urllib.request.urlopen(all_posts_req).read().decode('utf-8')
    all_posts_resp = json.loads(all_posts_resp_json)

    return render(request, 'frontend/all_posts.html', {"posts" : all_posts_resp})


def show_special_posts(request):
    all_posts_req = urllib.request.Request('http://exp:8000/posts/')
    all_posts_resp_json = urllib.request.urlopen(all_posts_req).read().decode('utf-8')
    all_posts_resp = json.loads(all_posts_resp_json)

    if (len(all_posts_resp) > 0):
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
    else:
        latest_post, cheapest_post, most_swipe_post = "N/A", "N/A", "N/A"

    flag = (len(all_posts_resp) > 0)

    return render(request, 'frontend/special_posts.html', {'latest_post' : latest_post, 'flag' : str(flag),
                                                    "cheapest_post" : cheapest_post, "most_swipe_post" : most_swipe_post})

def post_detail(request, pid):
    url = 'http://exp:8000/posts/' + str(pid) + "/"
    req = urllib.request.Request(url)
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)
    if (resp['ok']):
        return render(request, "frontend/post_detail.html", {'post': resp})
    else: 
        err_msg = "Sorry! This listing doesn't exist."
        return render(request, "frontend/post_detail.html", {'err_msg': err_msg})


def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            data = request.POST
            data = urllib.parse.urlencode(data).encode()
            req = urllib.request.Request('http://exp:8000/create_user/', data=data)
            resp_json = urllib.request.urlopen(req).read().decode('utf-8')
            resp = json.loads(resp_json)

            # handle signup error properly
            if not resp["ok"]:
                s = ""
                if resp["err_code"] == 2:
                    s = "Email already exists."
                elif resp["err_code"] == 3:
                    s = "Username already exists."
                messages.warning(request, s)
                # read user's previous inputs to pre-fill the form
                dummyuser = DummyUser.objects.create(
                    email = form.cleaned_data.get("email"),
                    username = form.cleaned_data.get("username"),
                    first_name = form.cleaned_data.get("first_name"),
                    last_name = form.cleaned_data.get("last_name"),
                    computing_id = form.cleaned_data.get("computing_id"),
                    phone_number = form.cleaned_data.get("phone_number"),
                    bio = form.cleaned_data.get("bio"))
                form = SignUpForm(instance=dummyuser)
                dummyuser.delete()
                return render(request, 'frontend/signup.html', {'form':form})
        
            username = resp['username']
            password = resp['password']
            auth = login_exp_api(username, password) 
            authenticator = auth['authenticator']

            s = "Account created for " + form.cleaned_data.get("username") + "!"
            messages.success(request, s)
            response = HttpResponseRedirect(reverse('frontend:login'))
            response.set_cookie("auth", authenticator)
            return response
            
    else:
        form = SignUpForm()
    return render(request, 'frontend/signup.html', {'form':form})


def login(request):
    # If we received a GET request instead of a POST request
    if request.method == 'GET':
        # display the login form page
        next = request.GET.get('next') or reverse('frontend:homepage')
        form = LogInForm()
        return render(request, 'frontend/login.html', {'form':form})

    # Creates a new instance of our login_form and gives it our POST data
    form = LogInForm(request.POST)

    # Check if the form instance is invalid
    if not form.is_valid():
      # Form was bad -- send them back to login page and show them an error
      return render(request, 'frontend/login.html', {'from':form})

    # Sanitize username and password fields
    username = form.cleaned_data['username']
    password = form.cleaned_data['password']

    # Get next page
    next = form.cleaned_data.get('next') or reverse('frontend:homepage')

    # Send validated information to our experience layer
    resp = login_exp_api(username, password)    

    # Check if the experience layer said they gave us incorrect information
    if not resp or not resp['ok']:
      # Couldn't log them in, send them back to login page with error
      form = LogInForm()
      if (resp['err_code'] == 0):
        messages.warning(request, "Username does not exist.")
      elif (resp['err_code'] == 1):
        messages.warning(request, "Your password does not match your username. Please try again.")
      else:
        messages.warning(request, "We failed to reach a server or the server couldn\'t fulfill the request.")
      return render(request, 'frontend/login.html', {"form":form})
    
    #return HttpResponse(resp) ###added for debug
    
    """ If we made it here, we can log them in. """
    # Set their login cookie and redirect to back to wherever they came from
    authenticator = resp['authenticator']
    first_name = resp['first_name']

    response = HttpResponseRedirect(next)

    response.set_cookie("auth", authenticator)
    response.set_cookie("first_name", first_name)
    response.set_cookie("logged_in", True)
    
    return response


def login_exp_api(username, password):
    data = {'username':username, 'password':password}
    data = urllib.parse.urlencode(data).encode()
    req = urllib.request.Request('http://exp:8000/login/', data=data)
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)
    return resp


def check_auth(authenticator):
    data = {'authenticator': authenticator}
    data = urllib.parse.urlencode(data).encode()
    req = urllib.request.Request('http://exp:8000/check_auth/', data=data)
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)
    return resp['ok']


def logout(request):
    url = 'http://exp:8000/delete/auth/' + request.COOKIES.get('auth')
    req = urllib.request.Request(url)
    try:
        resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    except HTTPError as e:
        print('e')
    response = HttpResponseRedirect(reverse ('frontend:logout_success'))
    response.delete_cookie("auth")
    response.delete_cookie("first_name")
    response.delete_cookie("logged_in")
    return response


def logout_success(request):
    return render(request, 'frontend/logout_success.html')


# def create_listing(request):
#     # Try to get the authenticator cookie
#     auth = request.COOKIES.get('auth')

#     # If the authenticator cookie wasn't set...
#     if not auth:
#       # Handle user not logged in while trying to create a listing
#       return HttpResponseRedirect(reverse("frontend:login") + "?next=" + reverse("frontend:create_listing"))

#     # If we received a GET request instead of a POST request...
#     if request.method == 'GET':
#         # Return to form page
#         form = CreatePostForm()
#         return render(request, "frontend/create_listing.html", {"form" : form})

#     # Otherwise, create a new form instance with our POST data
#     form = CreatePostForm(request.POST)

#     # Send validated information to our experience layer
#     resp = create_listing_exp_api(auth, ...)


# def create_listing_exp_api














