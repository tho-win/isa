from django.test import TestCase, Client
from django.utils import timezone
from django.test import TestCase
from django.urls import reverse
from .models import *
import datetime

from django.shortcuts import render, render_to_response
from django.http import HttpResponse, JsonResponse
import urllib.request
import urllib.parse
import json

USER_NAME = "tj1819"
COMPUTING_ID = "tj5ca"
FIRST_NAME = "Thomas"
LAST_NAME = "Jefferson"
EMAIL = COMPUTING_ID + "@virginia.edu"
PASSWORD = "pAsswrd123!!"
PHONE_NUMBER = "5555555555"
BIO = "I'M TJ!"

TITLE = "Test post"
CONTENT = "content"
PRICE = 2.0
SWIPES = 10


class CustomUserTest(TestCase):
	def setUp(self):
		self.test_user = CustomUser.objects.create_user(username=USER_NAME, email=EMAIL,
											first_name=FIRST_NAME, last_name=LAST_NAME, 
											password=PASSWORD, bio=BIO,
											phone_number=PHONE_NUMBER,computing_id=COMPUTING_ID,)

	def test_create_user(self):
		self.assertIn(self.test_user, CustomUser.objects.all(), "Check if user is created in database")

	def test_update_user(self):
		self.test_user.phone_number = "1234567890"
		self.test_user.save()
		self.assertNotEqual("5555555555", self.test_user.phone_number)

	def test_delete_user(self):
		self.test_user.delete()
		self.assertNotIn(self.test_user, CustomUser.objects.all())

	def test_user_to_string(self):
		self.assertEqual(str(self.test_user), USER_NAME)


class PostTest(TestCase):
	# Create a user through direct method calls for testing and create a post for the user
	def setUp(self):
		self.test_user = CustomUser.objects.create_user(username=USER_NAME, email=EMAIL,
											first_name=FIRST_NAME, last_name=LAST_NAME, 
											password=PASSWORD, bio=BIO,
											phone_number=PHONE_NUMBER, computing_id=COMPUTING_ID,)
		self.test_post = self.test_user.create_post(title="Test post", content="Description.", price=2.0, swipes=10)

	def test_create_post(self):
		self.assertIn(self.test_post, Post.objects.all(), "Check if post is created in database.")

	def test_update_post(self):
		self.test_post.content = "updated content"
		self.test_post.save()
		self.assertNotEqual("Description.", self.test_post.content)

	def test_delete_post(self):
		tmp_post = Post.objects.create(title="Temp Post", content="xxx", price=1.00,
										seller=self.test_user.username, seller_id = self.test_user.id, remaining_nums=10)
		tmp_post.save()
		self.assertIn(tmp_post, Post.objects.all())
		tmp_post.delete()
		self.assertNotIn(tmp_post, Post.objects.all())

	def test_post_to_string(self):
		self.assertEqual("Test post created by tj1819", str(self.test_post))

	def test_was_published_in_30days_future_post(self):
		future_time = timezone.now() + datetime.timedelta(days=30)
		future_post = Post(pub_date=future_time)
		self.assertFalse(future_post.was_published_in_30days())

	def test_was_published_in_30days_old_post(self):
		old_time = timezone.now() - datetime.timedelta(days=50)
		old_post = Post(pub_date=old_time)
		self.assertFalse(old_post.was_published_in_30days())

	def test_was_published_in_30days_recent_post(self):
		recent_time = timezone.now() - datetime.timedelta(days=10)
		recent_post = Post(pub_date=recent_time)
		self.assertTrue(recent_post.was_published_in_30days())

	def test_was_published_in_30days_edge_post(self):
		edge_time = timezone.now() - datetime.timedelta(days=30)
		edge_post = Post(pub_date=edge_time)
		self.assertFalse(edge_post.was_published_in_30days())

	def test_was_published_in_90days_future_post(self):
		future_time = timezone.now() + datetime.timedelta(days=180)
		future_post = Post(pub_date=future_time)
		self.assertFalse(future_post.was_published_in_90days())

	def test_was_published_in_90days_old_post(self):
		old_time = timezone.now() - datetime.timedelta(days=100)
		old_post = Post(pub_date=old_time)
		self.assertFalse(old_post.was_published_in_90days())

	def test_was_published_in_90days_recent_post(self):
		recent_time = timezone.now() - datetime.timedelta(days=10)
		recent_post = Post(pub_date=recent_time)
		self.assertTrue(recent_post.was_published_in_90days())

	def test_was_published_in_90days_edge_post(self):
		edge_time = timezone.now() - datetime.timedelta(days=90)
		edge_post = Post(pub_date=edge_time)
		self.assertFalse(edge_post.was_published_in_90days())


class APITest(TestCase):
	def setUp(self):
		self.test_user = CustomUser.objects.create(username=USER_NAME, email=EMAIL,
											first_name=FIRST_NAME, last_name=LAST_NAME, 
											password=PASSWORD, bio=BIO,
											phone_number=PHONE_NUMBER, computing_id=COMPUTING_ID,)
		self.test_post = self.test_user.create_post(title=TITLE, content=CONTENT, price=PRICE, swipes=SWIPES)
		self.school = School.objects.create(name="UVA", city="Charlottesville", state="VA")

	def test_success_response_list(self):
		response_root = self.client.get(reverse("api-root"))
		self.assertEqual(response_root.status_code, 200)
		response_user = self.client.get(reverse("customuser-list"))
		self.assertEqual(response_user.status_code, 200)
		response_post = self.client.get(reverse("post-list")) 
		self.assertEqual(response_post.status_code, 200)
		response_school = self.client.get(reverse("school-list")) 
		self.assertEqual(response_school.status_code, 200)

	def test_success_response_user_instance(self):
		response = self.client.get(reverse("customuser-detail", kwargs={"pk":self.test_user.id}))
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.json()["username"], USER_NAME)
		
	def test_success_response_post_instance(self):
		response = self.client.get(reverse("post-detail", kwargs={"pk":self.test_post.id}))
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.json()["title"], TITLE)

	def test_success_response_school_instance(self):
		response = self.client.get(reverse("school-detail", kwargs={"pk":self.school.id}))
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.json()["name"], "UVA")

	def test_success_response_add_instance(self):
		temp_school = School.objects.create(name="Cornell", city="Ithaca", state="NY")
		temp_school.save()
		response_list = self.client.get(reverse("school-list")) 
		self.assertEqual(len(response_list.json()), 2)
		self.assertContains(response_list, "Cornell")

	def test_success_response_update_instance(self):
		self.test_user.phone_number = "1234567890"
		self.test_user.save()
		response = self.client.get(reverse("customuser-detail", kwargs={"pk":self.test_user.id}))
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.json()["phone_number"], "1234567890")

	def test_success_response_delete_instance(self):
		temp_post = Post.objects.create(seller=self.test_user.username, seller_id = self.test_user.id, title="temp title", 
										content="temp content", price=1, remaining_nums=10)
		temp_post.save()
		response_before_delete = self.client.get(reverse("post-list")) 
		self.assertContains(response_before_delete, "temp content")
		temp_post.delete()
		response_after_delete = self.client.get(reverse("post-list")) 
		self.assertEqual(response_after_delete.status_code, 200)
		self.assertEqual(len(response_after_delete.json()),1)
		self.assertNotContains(response_after_delete, "temp content")

	def test_success_response_json_format(self):
		response = self.client.get("http://models:8000/api/v1/school/?format=json")
		self.assertEqual(response.json()[0]["name"], "UVA")

	def test_failed_response_wrong_pk_no_instance(self):
		response = self.client.get(reverse("customuser-detail", kwargs={"pk":9999}))
		self.assertEqual(response.status_code, 404)

	def test_failed_response_wrong_pk_wrong_type(self):
		response = self.client.get(reverse("post-detail", kwargs={"pk":"UVAUVAUVA"}))
		self.assertEqual(response.status_code, 404)

	def test_failed_response_wrong_url(self):
		response_user = self.client.get("http://models:8000/api/v1/users/") 
		self.assertEqual(response_user.status_code, 404)
		response_post = self.client.get("http://models:8000/api/v1/posts/") 
		self.assertEqual(response_post.status_code, 404)
		response_school = self.client.get("http://models:8000/api/v1/schools/") 
		self.assertEqual(response_school.status_code, 404)
		response_v2 = self.client.get("http://models:8000/api/v2/user/") 
		self.assertEqual(response_v2.status_code, 404)
		response_random = self.client.get("http://models:8000/randomstuffblabla/") 
		self.assertEqual(response_random.status_code, 404)

