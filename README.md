# TwitterApi
Creating Api app for twitter.
installing require from requirements
using tweepy lib.
Database:
Created restful database in localhost MySql.
created 2 tables, users and posts (one to many).
tweepy:
for tweepy u need to change from file config
conusmerkey, consumersecret, access_token,access_token_secret
urls:
http://localhost:5000/users/
get saved users and return from table MySql
http://localhost:5000/users/twitterId/
scrap and saved in db
if local true
scarped json
http://localhost:5000/users/twitterId/posts
return 25 tweet
saved in db
if local = true:
saved and return from data bases
to run using:
python twitter.py
for test cases not completed now
