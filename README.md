This is a group project for CS 4260: Internet Scale Application at University of Virginia in Spring 2020 semester.

Contact Info:

Tho Nguyen (tnn7yc@virginia.edu); Erik Toor (evt8ed@virginia.edu); Haoran Zhu (hz3fr@virginia.edu)

Frontend:

http://localhost:8000/ is the homepage.

http://localhost:8000/about shows basic information about our marketplace.

http://localhost:8000/users/ shows some basic info about all users available in the dataset for demo purposes.

http://localhost:8000/posts/ shows some basic info about all posts available in the dataset for demo purposes.

http://localhost:8000/specialposts shows the latest post, post with most remaining swipes and lowest prices.

http://localhost:8000/signup is the sign up page for user to create new account.

http://localhost:8000/login is the page signed up users use to log in.

Services:

As of 03/02/2020, the API supports services for User, Post and School models:

http://localhost:8001/api/v1/ GET to show supported services

http://localhost:8001/api/v1/user/ GET to show all User intances, POST to add create user

http://localhost:8001/api/v1/user/1/ GET to show user with id=1, PUT to edit or DELETE to delete user instance

Similarly, replace "user" keyword with "post" or "school" to play with School models :)

Update as of Project 4 (3/25/2020):

The website allows user to create new account (sign up), login, logout, creating new listing and display Profile page.
