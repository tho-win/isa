import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

USER_NAME = "test_user"
COMPUTING_ID = "test"
FIRST_NAME = "Test"
LAST_NAME = "User"
EMAIL = COMPUTING_ID + "@virginia.edu"
PASSWORD = "pAsswrd123!!"
PHONE_NUMBER = "5555555555"
BIO = "I'm a test user.!"

TITLE = "Test post"
CONTENT = "content"
PRICE = 2.0
SWIPES = 10

# class DisplayTest(unittest.TestCase):
# 	def setUp(self):
# 		# 'http://selenium-chrome:4444/wd/hub'
# 		self.driver = webdriver.Remote(command_executor='http://localhost:4444/wd/hub', 
# 			desired_capabilities=DesiredCapabilities.CHROME)

# 	def test_homepage(self): 
# 		self.driver.get("http://64.225.30.56:8000/")
# 		self.assertIn("Home", self.driver.title)

# 	def test_login(self): 
# 		self.driver.get("http://64.225.30.56:8000/login/")
# 		self.assertIn("Log In", self.driver.title)

# 	def test_signup(self): 
# 		self.driver.get("http://64.225.30.56:8000/signup/")
# 		self.assertIn("Sign Up", self.driver.title)

# 	def tearDown(self):
# 		self.driver.close()

class ASignUpTest(unittest.TestCase):
	def setUp(self):
		self.driver = webdriver.Remote(command_executor='http://localhost:4444/wd/hub', 
			desired_capabilities=DesiredCapabilities.CHROME)

	def fill_out_sign_up(self):
		first_name = self.driver.find_element_by_name("first_name")
		first_name.send_keys(FIRST_NAME)
		last_name = self.driver.find_element_by_name("last_name")
		last_name.send_keys(LAST_NAME)
		username = self.driver.find_element_by_name("username")
		username.send_keys(USER_NAME)
		email = self.driver.find_element_by_name("email")
		email.send_keys(EMAIL)
		password = self.driver.find_element_by_name("password")
		password.send_keys(PASSWORD)
		computing_id = self.driver.find_element_by_name("computing_id")
		computing_id.send_keys(COMPUTING_ID)
		phone_number = self.driver.find_element_by_name("phone_number")
		phone_number.send_keys(PHONE_NUMBER)
		bio = self.driver.find_element_by_name("bio")
		bio.send_keys(BIO)
		bio.submit()

	def test_a_sign_up_success(self):
		self.driver.get("http://64.225.30.56:8000/signup/")
		self.fill_out_sign_up()
		self.assertIn("Account created for test_user", self.driver.page_source)

	def test_b_sign_up_email_taken(self):
		self.driver.get("http://64.225.30.56:8000/signup/")
		first_name = self.driver.find_element_by_name("first_name")
		first_name.send_keys(FIRST_NAME)
		last_name = self.driver.find_element_by_name("last_name")
		last_name.send_keys(LAST_NAME)
		username = self.driver.find_element_by_name("username")
		username.send_keys("test_user_2")
		email = self.driver.find_element_by_name("email")
		email.send_keys(EMAIL)
		password = self.driver.find_element_by_name("password")
		password.send_keys(PASSWORD)
		computing_id = self.driver.find_element_by_name("computing_id")
		computing_id.send_keys(COMPUTING_ID)
		phone_number = self.driver.find_element_by_name("phone_number")
		phone_number.send_keys(PHONE_NUMBER)
		bio = self.driver.find_element_by_name("bio")
		bio.send_keys(BIO)
		bio.submit()
		self.assertNotIn("Account created for test_user_2", self.driver.page_source)

	def test_c_sign_up_username_taken(self):
		self.driver.get("http://64.225.30.56:8000/signup/")
		first_name = self.driver.find_element_by_name("first_name")
		first_name.send_keys(FIRST_NAME)
		last_name = self.driver.find_element_by_name("last_name")
		last_name.send_keys(LAST_NAME)
		username = self.driver.find_element_by_name("username")
		username.send_keys("test_user")
		email = self.driver.find_element_by_name("email")
		email.send_keys("xxxxx@gmail.com")
		password = self.driver.find_element_by_name("password")
		password.send_keys(PASSWORD)
		computing_id = self.driver.find_element_by_name("computing_id")
		computing_id.send_keys(COMPUTING_ID)
		phone_number = self.driver.find_element_by_name("phone_number")
		phone_number.send_keys(PHONE_NUMBER)
		bio = self.driver.find_element_by_name("bio")
		bio.send_keys(BIO)
		bio.submit()
		self.assertNotIn("Account created for test_user", self.driver.page_source)

	def tearDown(self):
		self.driver.close()	


class BLogInTest(unittest.TestCase):
	def setUp(self):
		self.driver = webdriver.Remote(command_executor='http://localhost:4444/wd/hub', 
			desired_capabilities=DesiredCapabilities.CHROME)

	def fill_out_log_in(self):
		username = self.driver.find_element_by_name("username")
		username.send_keys(USER_NAME)
		password = self.driver.find_element_by_name("password")
		password.send_keys(PASSWORD)
		password.submit()

	def test_a_log_in_success(self):
		time.sleep(3)
		self.driver.get("http://64.225.30.56:8000/login/")
		self.fill_out_log_in()
		self.assertIn("Profile", self.driver.page_source)
		self.assertIn("Log out", self.driver.page_source)

	def test_b_log_in_username_not_exist(self):
		self.driver.get("http://64.225.30.56:8000/login/")
		username = self.driver.find_element_by_name("username")
		username.send_keys("sndhvfbnms")
		password = self.driver.find_element_by_name("password")
		password.send_keys(PASSWORD)
		self.assertNotIn("Profile", self.driver.page_source)
		self.assertNotIn("Log out", self.driver.page_source)

	def test_c_log_in_password_incorrect(self):
		self.driver.get("http://64.225.30.56:8000/login/")
		username = self.driver.find_element_by_name("username")
		username.send_keys(USER_NAME)
		password = self.driver.find_element_by_name("password")
		password.send_keys("PASSWORD")
		self.assertNotIn("Profile", self.driver.page_source)
		self.assertNotIn("Log out", self.driver.page_source)

	def tearDown(self):
		self.driver.close()	


class CSearchTest(unittest.TestCase):
	def setUp(self):
		self.driver = webdriver.Remote(command_executor='http://localhost:4444/wd/hub', 
			desired_capabilities=DesiredCapabilities.CHROME)

	
	def tearDown(self):
		self.driver.close()	

if __name__ == "__main__":
	unittest.main()



