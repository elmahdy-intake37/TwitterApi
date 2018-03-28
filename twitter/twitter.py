from flask import Flask, flash, request, redirect, render_template, url_for
from flaskext.mysql import MySQL
import tweepy
import json
from config import *



DEBUG = True
mysql = MySQL()
app = Flask(__name__)
app.debug = DEBUG



# Creating the authentication object
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
# Setting your access token and secret
auth.set_access_token(access_token, access_token_secret)
# Creating the API object while passing in auth information
api = tweepy.API(auth, wait_on_rate_limit=True)


#MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'restful'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)




conn = mysql.connect()
if conn:
    print("sucess")
else:
    print("failed")

cursor = conn.cursor()
def create_tables():
    query ="CREATE TABLE if not exists users (id INT PRIMARY KEY auto_increment,\
            userId int ,username VARCHAR(40))"
    cursor.execute(query)
    conn.commit()
    query ="CREATE TABLE if not exists  posts (id INT  PRIMARY KEY  auto_increment,\
            Dates date, post text not null, user_id INT, \
            FOREIGN KEY (user_id) REFERENCES users(id))"
    cursor.execute(query)
    conn.commit()
    conn.close()
    return "created tables"

@app.route('/users/')
def list_user():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute('''select * from users''')
    obj = cursor.fetchall()
    conn.close()
    loader_r= json.dumps(obj)
    data = json.loads(loader_r)
    return render_template('index.html', data=data)


@app.route('/users/<int:twitter_id>')
def scrap(twitter_id):
    conn = mysql.connect()
    cursor = conn.cursor()
    localparam = request.args.get('local')
    scrap_data = api.user_timeline(id=twitter_id)
    for tweet in scrap_data:
        dates = tweet.created_at
        name = tweet.user.name
        tweets = tweet.text
        Id = tweet.id
        cursor.execute('''select username, post from users inner join posts on users.id = posts.id''')
        obj = cursor.fetchall()
        ob_name= obj[0]
        ob_post= obj[1]
        if ob_name == name and ob_post == tweets:
            pass
        elif ob_name == name and ob_post != tweets:
            cursor.execute('''update posts inner joinn users on users.id = posts.id set post = (%s) where username =(%s)''',(tweets, name))
            conn.commit
        else:
            cursor.execute('''INSERT INTO users(userId, username) VALUES (%s, %s)''',(Id, name))
            cursor.execute('''INSERT INTO posts (Dates, post) VALUES (%s, %s)''', (dates, tweets))
            conn.commit

    if localparam == "true":
        return "scraped"
    else:
        cursor.execute('''select username, post from users inner join posts on users.id = posts.id''')
        obj = cursor.fetchall()
        conn.close()
        r = json.dumps(obj)
        return r
#
PER_PAGE = 20

# @app.route('/users/', defaults={'page': 1})
@app.route('/users/<int:twitter_id>/posts')
def data_user(twitter_id):
    data = {}
    i = 0
    conn = mysql.connect()
    cursor = conn.cursor()
    localparam = request.args.get('local')
    data_user = api.user_timeline(id=twitter_id, count=25)
    localparam = request.args.get('local')
    for tweet in data_user:
        dates = tweet.created_at
        name = tweet.user.name
        tweets = tweet.text
        data[i]= tweets
        Id = tweet.id
        i +=1
        cursor.execute('''INSERT INTO users(userId, username) VALUES (%s, %s)''',(Id, name))
        cursor.execute('''INSERT INTO posts (Dates, post) VALUES (%s, %s)''', (dates, tweets))
        conn.commit
        cursor.execute('''select username, post from users inner join posts on users.id = posts.id''')
        obj = cursor.fetchall()
        ob_name= obj[0]
        ob_post= obj[1]
        if ob_name == name and ob_post == tweets:
            pass
        elif ob_name == name and ob_post != tweets:
            cursor.execute('''update posts inner joinn users on users.id = posts.id set post = (%s) where username =(%s)''',(tweets, name))
            conn.commit
        else:
            cursor.execute('''INSERT INTO users(userId, username) VALUES (%s, %s)''',(Id, name))
            cursor.execute('''INSERT INTO posts (Dates, post) VALUES (%s, %s)''', (dates, tweets))
            conn.commit
    if  localparam == 'true':
        cursor.execute('''select post from users inner join posts on users.id = posts.id where username = (%s)''',(name))
        obj = cursor.fetchall()
        conn.close()
        loader_r= json.dumps(obj)
        data = json.loads(loader_r)
        return render_template('index.html', data=data)
    else:
        return render_template('index.html', data=data)



    # cursor.execute('''SELECT * from users LEFT JOIN posts on posts.user_id = users.id \
    # union select * from users right join posts on posts.user_id = users.id \
    # where userId =(%s) ''', (twitter_id))
    # obj = cursor.fetchall()
    # print("obj ====", obj)
    # cursor.execute('''drop tables posts''')
    # cursor.execute('''drop tables users''')
    # conn.commit()

    # r = json.dumps(obj)
    # loader_r = json.loads(r)


if __name__ == "__main__":
    print((create_tables()))
    app.run()
