This is a group project for CS 4260: Internet Scale Application at University of Virginia in Spring 2020 semester.

### Contact Info: ###
--------------

Tho Nguyen (tnn7yc@virginia.edu); Erik Toor (evt8ed@virginia.edu); Haoran Zhu (hz3fr@virginia.edu)

### Newest update for project 7: ###
--------------

- recommendation.py is responsible for extracting recommendation info from access log and organizing them into a recommendation table. Both recommendation.py and access log are in access_log folder.

- Recommendation table is created every time recommendation.py runs. It's then saved to recommendation_table.csv.

- automate.sh runs recommendation.py automatically every two minutes. It's in app folder.

### Useful URLs to naivgate the app: ###
--------------

Frontend:

http://localhost:8000/ is the homepage.

http://localhost:8000/about shows basic information about our marketplace.

http://localhost:8000/users/ shows some basic info about all users available in the dataset for demo purposes.

http://localhost:8000/posts/ shows some basic info about all posts available in the dataset for demo purposes.

http://localhost:8000/specialposts shows the latest post, post with most remaining swipes and lowest prices.

http://localhost:8000/signup is the sign up page for user to create new account.

http://localhost:8000/login is the page for signed up users use to log in.

http://localhost:8000/logout is the page for signed in user to log out their account

http://localhost:8000/profile is the page for signed in user to view thier profile

http://localhost:8000/profile_update is the page for signed in user to update their profile

http://localhost:8000/create_listing is the page for signed in user to create a new listing

Services:

As of 03/02/2020, the API supports services for User, Post and School models:

http://localhost:8001/api/v1/ GET to show supported services

http://localhost:8001/api/v1/user/ GET to show all User intances, POST to add create user

http://localhost:8001/api/v1/user/1/ GET to show user with id=1, PUT to edit or DELETE to delete user instance

Similarly, replace "user" keyword with "post" or "school" to play with Post, School models :)


**web container**: http://localhost:8000/search_listing is the page for users to search for listings by typing their queries

**batch container**: batch.py file is the script for adding newly created listings into kafka queuing system

**access_log container**: post_view.py is the script for accumulating clicks on any particular listing, which are then used to determine the ranking for search results

**Note:** 
- We did NOT include user_id in the access log as we believe that it would be more reasonable to also include non-logged in users' clicks when considering ranking.

- It might take a while for scripts in batch/access_log container to process the addition to queue and for the queue to add those items into ES.

- http://64.225.30.56/ is the newest URL for our app.

- Integration tests are also developed for the above URL. 

- When you make a commit, it takes 4-5 minutes for Travic CI to test the build. 

- Integration tests are run in Travic CI using the command: "python ./selenium/selenium_test.py". So look the results under that command for integration test results.

- Unit tests are included in docker compose.
