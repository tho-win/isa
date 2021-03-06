from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from urllib.error import URLError, HTTPError
from .forms import SignUpForm, LogInForm, CreatePostForm, ProfileUpdateForm
from django.shortcuts import render, render_to_response
from django.views.generic import TemplateView
from .models import DummyUser
from django.contrib import messages
from django.urls import reverse
import urllib.request
import urllib.parse
import datetime
import json
import socket


def get_uid_by_auth(auth):
    req = urllib.request.Request('http://exp:8000/authenticators/')
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)
    user_id = -1
    for item in resp:
        if item['authenticator'] == auth:
            user_id = item['user_id']
            break
    return user_id


def get_username_by_auth(auth):
    user_id = get_uid_by_auth(auth)
    username_url = 'http://exp:8000/users/' + str(user_id) + "/"
    req = urllib.request.Request(username_url)
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)
    username = ""
    if "error status" in resp.keys():
        username = "NULL"
        return username
    username = resp['username']
    return username


def homepage(request):
    all_posts_req = urllib.request.Request('http://exp:8000/posts/')
    # all_posts_resp_json = urllib.request.urlopen(all_posts_req).read().decode('utf-8')
    try:
        response = urllib.request.urlopen(all_posts_req)
    except urllib.error.URLError as e:
        err_resp = {"error status" : e.code, "error reason": e.reason}
        messages.info(request, e.reason)
        return render(request, 'frontend/homepage.html')
    all_posts_resp_json = response.read().decode('utf-8')
    all_posts_resp = json.loads(all_posts_resp_json)
    if "error status" in all_posts_resp[0].keys():
        return render(request, 'frontend/homepage.html')
    auth = request.COOKIES.get('auth')
    special_posts = show_special_posts(request)
    if auth:
        if check_auth(auth):
            return render(request, 'frontend/homepage.html', {'posts': all_posts_resp, 'special_posts_flag': special_posts['flag'],
                'latest_post' : special_posts['latest_post'], "cheapest_post" : special_posts['cheapest_post'], 
                "most_swipe_post" : special_posts['most_swipe_post']})

    return render(request, 'frontend/homepage.html', {'posts': all_posts_resp, 'special_posts_flag': special_posts['flag'],
        'latest_post' : special_posts['latest_post'], "cheapest_post" : special_posts['cheapest_post'], 
        "most_swipe_post" : special_posts['most_swipe_post']})


def about(request):
    return render(request, 'frontend/about.html')

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
    err = False
    if "error status" in resp.keys():
        err = True
    else:
        resp.pop("url")
        resp.pop("password")
    return render(request, "frontend/user_detail.html", {'user': resp, 'err': err})


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
    return {'latest_post' : latest_post, 'flag' : str(flag), "cheapest_post" : cheapest_post, "most_swipe_post" : most_swipe_post}
    '''
    return render(request, 'frontend/special_posts.html', {'latest_post' : latest_post, 'flag' : str(flag),
                                                    "cheapest_post" : cheapest_post, "most_swipe_post" : most_swipe_post})
    '''

def get_posts_by_seller(seller_id):
    url = 'http://exp:8000/posts_by_seller/' + str(seller_id) + '/'
    req = urllib.request.Request(url)
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)
    return resp


def post_detail(request, pid):
    url = 'http://exp:8000/posts/' + str(pid) + "/"
    req = urllib.request.Request(url)
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)

    if request.COOKIES.get('logged_in'):
        data = {'user_id' : get_uid_by_auth(request.COOKIES.get('auth')), 'listing_id' : pid}
        data = urllib.parse.urlencode(data).encode()
        view_req = urllib.request.Request('http://exp:8000/listing_views/', data=data)
        try:
            view_response = urllib.request.urlopen(view_req)
        except urllib.error.URLError as e:
            messages.info(request, "Updating access log failed!")
            if resp['ok']:
                return render(request, "frontend/post_detail.html", {'post': resp})
            return render(request, "frontend/post_detail.html")
        view_resp_json = view_response.read().decode('utf-8')
        view_resp = json.loads(view_resp_json)

    if resp['ok']:
        recomm_url = 'http://exp:8000/get_recomm/' + str(pid) + '/'
        recomm_req = urllib.request.Request(recomm_url)
        try:
            recomm_response = urllib.request.urlopen(recomm_req)
        except urllib.error.URLError as e:
            messages.warning(request, "failed to load recommendations in exp layer")
            return render(request, "frontend/post_detail.html", {'post': resp})
        else:
            recomm_resp_json = recomm_response.read().decode('utf-8')
            recomm_resp = json.loads(recomm_resp_json)
            if recomm_resp['ok']:
                recommendations = recomm_resp['recomm']
                return render(request, "frontend/post_detail.html", {'post': resp, 'recommendations': recommendations})
            else:
                if 'err_reason' in recomm_resp:
                    messages.warning(request, "failed to load recommendations in model layer")
                return render(request, "frontend/post_detail.html", {'post': resp})
    else:
        return render(request, "frontend/post_detail.html") 


def sign_up(request):
    if request.COOKIES.get('logged_in'):
        messages.info(request, 'You must log out first to sign up for another account.')
        return HttpResponseRedirect(reverse('frontend:homepage'))
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            data = request.POST
            if ' ' in form.cleaned_data.get("username"):
                messages.warning(request, "Username contains illegal character. Please use another username.")
                dummyuser = DummyUser.objects.create(
                    email = form.cleaned_data.get("email"),
                    username = form.cleaned_data.get("username"),
                    first_name = form.cleaned_data.get("first_name"),
                    last_name = form.cleaned_data.get("last_name"),
                    computing_id = form.cleaned_data.get("computing_id"),
                    phone_number = form.cleaned_data.get("phone_number"),
                    bio = form.cleaned_data.get("bio"))
                empty_form = SignUpForm(instance=dummyuser)
                dummyuser.delete()
                return render(request, 'frontend/signup.html', {'form': empty_form})
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
        
            s = "Account created for " + form.cleaned_data.get("username") + "!"
            messages.success(request, s)
            response = HttpResponseRedirect(reverse('frontend:login'))
            return response
    else:
        form = SignUpForm()
    return render(request, 'frontend/signup.html', {'form':form})


def login(request):
    if request.COOKIES.get('logged_in'):
        messages.info(request, 'You must log out first to log in another account.')
        return HttpResponseRedirect(reverse('frontend:homepage'))
    # If we received a GET request instead of a POST request
    if request.method == 'GET':
        # display the login form page
        # mynext = request.GET.get('next') or reverse('frontend:homepage')
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

    # Send validated information to our experience layer
    resp = login_exp_api(username, password)    

    # Check if the experience layer said they gave us incorrect information
    if not resp or not resp['ok']:
      # Couldn't log them in, send them back to login page with error
      form = LogInForm()
      if resp['err_code']:
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
    user_id = resp['user_id']

    mynext = request.GET.get('next') 
    response = HttpResponseRedirect(reverse('frontend:homepage'))
    if mynext:
         response = HttpResponseRedirect(mynext)

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


def create_listing(request):
     # Try to get the authenticator cookie
    auth = request.COOKIES.get('auth')
    logged_in = request.COOKIES.get('logged_in')
    # If the authenticator cookie wasn't set...
    if not logged_in:
        # Handle user not logged in while trying to create a listing
        messages.info(request, "Please log in your account to create a post.")
        return HttpResponseRedirect(reverse("frontend:login") + "?next=" + reverse("frontend:create_listing"))

    empty_form = CreatePostForm()
    if request.method == 'POST':
        form = CreatePostForm(request.POST)
        if form.is_valid():
            data = {}
            data['title'] = form.cleaned_data.get('title')
            data['content'] = form.cleaned_data.get('content')
            data['price'] = form.cleaned_data.get('price')
            data['remaining_nums'] = form.cleaned_data.get('remaining_nums')
            data['pickup_address'] = form.cleaned_data.get('pickup_address')

            data['seller'] = get_username_by_auth(request.COOKIES.get('auth'))
            data['seller_id'] = get_uid_by_auth(request.COOKIES.get('auth'))

            data = urllib.parse.urlencode(data).encode()
            req = urllib.request.Request('http://exp:8000/create_listing/', data=data)
            try:
                response = urllib.request.urlopen(req)
            except urllib.error.URLError as e:
                messages.warning(request, "We failed to reach a server or the server couldn\'t fulfill the request3.")
                return render(request, 'frontend/create_listing.html', {"form":empty_form})
            resp_json = response.read().decode('utf-8')
            resp = json.loads(resp_json)

            if not resp[0]['ok']:
                messages.warning(request, "We failed to reach a server or the server couldn\'t fulfill the request4.")
                return render(request, 'frontend/create_listing.html', {"form":empty_form})
            messages.success(request, "Your post has been created.")
            return HttpResponseRedirect(reverse('frontend:homepage'))

    return render(request, "frontend/create_listing.html", {"form":empty_form})


def profile(request):
    auth = request.COOKIES.get('auth')
    if not auth:
        messages.info(request, "Please log in your account to view your profile.")
        return HttpResponseRedirect(reverse("frontend:login") + "?next=" + reverse("frontend:profile"))

    username = get_username_by_auth(auth)
    user_id = get_uid_by_auth(auth)
    url = 'http://exp:8000/users/' + str(user_id) + "/"
    req = urllib.request.Request(url)
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)
    if "error status" in resp.keys():
        messages.info(request, "Sorry, we failed to authenticate your account. Please log in again.")
        return HttpResponseRedirect(reverse("frontend:logout"))
    date_joined = resp['date_joined'][:10]
    resp['date_joined'] = date_joined
    resp.pop('url')
    resp.pop('password')
    posts = get_posts_by_seller(user_id)
    if posts['ok']:
        resp['posts'] = posts['posts']

    return render(request, "frontend/profile.html", resp)


def profile_update(request):
    auth = request.COOKIES.get('auth')
    if not auth:
        messages.info(request, "Please log in your account to update your profile.")
        return HttpResponseRedirect(reverse("frontend:login") + "?next=" + reverse("frontend:profile"))

    # get current user information 
    username = get_username_by_auth(auth)
    user_id = get_uid_by_auth(auth)
    url = 'http://exp:8000/users/' + str(user_id) + "/"
    req = urllib.request.Request(url)
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)
    if "error status" in resp.keys():
        messages.info(request, "Sorry, we failed to authenticate your account. Please log in again.")
        return HttpResponseRedirect(reverse("frontend:logout"))

    # create a dummyuser to pre-fill the form
    dummyuser = DummyUser.objects.create(
                    email = resp["email"],
                    username = resp["username"],
                    first_name = resp["first_name"],
                    last_name = resp["last_name"],
                    computing_id = resp["computing_id"],
                    phone_number = resp["phone_number"],
                    bio = resp["bio"])

    null_form = ProfileUpdateForm(instance=dummyuser)
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=dummyuser)   
        if form.is_valid():
            data = {}
            data['id'] = user_id
            data['username'] = form.cleaned_data.get('username')
            data['email'] = form.cleaned_data.get('email')
            data['first_name'] = form.cleaned_data.get('first_name')
            data['last_name'] = form.cleaned_data.get('last_name')
            data['computing_id'] = form.cleaned_data.get('computing_id')
            data['phone_number'] = form.cleaned_data.get('phone_number')
            data['bio'] = form.cleaned_data.get('bio')

            data = urllib.parse.urlencode(data).encode()
            req = urllib.request.Request('http://exp:8000/profile_update/', data=data)
            try:
                response = urllib.request.urlopen(req)
            except urllib.error.URLError as e:
                dummyuser.delete()
                messages.info(request, "Sorry, we failed to update your profile. Please log in again.")
                return render(request, "frontend/profile_update.html", {"form" : null_form})

            resp_json = response.read().decode('utf-8')
            resp = json.loads(resp_json)
            dummyuser.delete()
            if not resp['ok']:
                if resp['err_code'] == 3:
                    messages.info(request, "Username " + form.cleaned_data.get('username') + " is already taken. Please try another one.")
                elif resp['err_code'] == 2:
                    messages.info(request, "Email " + form.cleaned_data.get('email') + " is already taken. Please try another one.")
                return render(request, "frontend/profile_update.html", {"form" : null_form})

            messages.success(request, "Your account has been updated.")
            response = HttpResponseRedirect(reverse("frontend:profile"))
            response.set_cookie("username", form.cleaned_data.get('username'))
            response.set_cookie("first_name", form.cleaned_data.get('first_name'))
            return response

    dummyuser.delete()
    return render(request, "frontend/profile_update.html", {"form" : null_form})

def search_listing(request):
    if request.method == 'POST':
        query = request.POST.get('search')
        data = {'query': query}
        data = urllib.parse.urlencode(data).encode()
        req = urllib.request.Request('http://exp:8000/search_listing/', data=data)
        response = urllib.request.urlopen(req)
        resp_json = response.read().decode('utf-8')
        resp = json.loads(resp_json)
        if not 'result' in resp:
            return render(request, "frontend/search_result.html", {'query': query})
        recall = resp['result']
        sorted_listings = [recall[0]]
        for i in range(1, len(recall)):
            listing = recall[i]["listing"]
            score = recall[i]["score"]
            for j in range(0, len(sorted_listings)):
                if score >= sorted_listings[j]["score"]:
                    sorted_listings.insert(j, recall[i])
                    break
                elif score < sorted_listings[len(sorted_listings)-1]["score"]:
                    sorted_listings.append(recall[i])
                    break
        final_list = []
        for item in sorted_listings:
            final_list.append(item["listing"])

        # messages.success(request, resp['raw_recall'])
        if resp['ok']:
            return render(request, "frontend/search_result.html", {'query': query, 'result': final_list})
    return render(request, "frontend/search_result.html", {'query': query})

    