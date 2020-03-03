This is a group project for CS 4260: Internet Scale Application at University of Virginia in Spring 2020 semester.

Contact Info:

Tho Nguyen (tnn7yc@virginia.edu); Erik Toor (evt8ed@virginia.edu); Haoran Zhu (hz3fr@virginia.edu)

Frontend:

http://localhost:8000/ is the homepage.

http://localhost:8000/users/ shows some basic info about all users available in the dataset for demo purposes.

http://localhost:8000/posts/ shows some basic info about all posts available in the dataset for demo purposes.

http://localhost:8000/specialposts shows the latest post, post with most remaining swipes and lowest prices.

Services:

As of 03/02/2020, the API supports services for User, Post and School models:

http://localhost:8001/api/v1/ GET to show supported services

http://localhost:8001/api/v1/user/ GET to show all User intances, POST to add create user

http://localhost:8001/api/v1/user/1/ GET to show user with id=1, PUT to edit or DELETE to delete user instance

Similarly, replace "user" keyword with "school" to play with School models :)
