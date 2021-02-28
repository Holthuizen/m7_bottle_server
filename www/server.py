
import bottle 
from bottle import route, run, get, post, redirect, template, SimpleTemplate
import requests as request 
import json

#security 
import secrets
import hashlib


'''SETUP ---------------------------------------------------------------------''' 
CONFIG = None
with open('config.txt') as json_file:
    CONFIG = json.load(json_file)
     
#base url
SERVER_URL = f"http://{CONFIG['host']}:{CONFIG['port']}"

#views 
bottle.TEMPLATE_PATH.append('./views/member')


'''SETUP -----------------------------------------------------------------''' 
#views
@get('/')
def index():
    return template('index', server_url = SERVER_URL)

'''Auth ---------------------------------------------------------------------''' 
from Auth import Authenticate
Auth = Authenticate(CONFIG['secret'],'http://localhost:1337')

#login view
@get('/login')
def login():
    return template('login')

# login logic
@post('/login')
def login():
    username = bottle.request.forms.get("username")
    pw = bottle.request.forms.get("password")
    
    if Auth.login(username,pw):
        return redirect(SERVER_URL+'/member')
    else: 
        redirect(SERVER_URL+"/login")

# logout logic
@get('/logout')
def logout():
    if Auth.auth():
        Auth.logout()
    redirect(SERVER_URL)
'''Auth ---------------------------------------------------------------------''' 

'''Member---------------------------------------------------------------------''' 
from Question import Question

@post("/member/question/create")
def submit_question(): 

    if not Auth.auth():
        print("no token pressend") 
        redirect(SERVER_URL+"/login")
  
    #read form data
    data = {}
    data['title'] = bottle.request.forms.get("title")
    data['description'] = bottle.request.forms.get("description")
    data['question'] = bottle.request.forms.get("question")

    #validation..

    #send data to strapi 
    q = Question()
    #jwt, data
    res = q.create(Auth.auth(),data)
    _id =  res.json()['id']  or 0 # todo return only a view of the question
    redirect(f"{SERVER_URL}/member/questions")


#protected routes: 

@get('/member')
def index():
    if not Auth.auth(): 
        redirect(SERVER_URL+"/login")
    return template('member/index', server_url = SERVER_URL)

@get('/member/questions')
def index():
    if not Auth.auth(): 
        redirect(SERVER_URL+"/login")
    #pull in questions
    q = Question()
    if q.status_code == 200: 
        r = q.read()
        data = r.json()
        return template('member/questions', server_url = SERVER_URL, data=data)


@get('/member/question/create')
def index():
    if not Auth.auth(): 
        redirect(SERVER_URL+"/login")
    return template('member/create_question_form', server_url = SERVER_URL)   




'''START SERVER---------------------------------------------------------------------''' 
run(host='localhost', port=CONFIG['port'], debug=True, reload=True)


#https://strapi.io/documentation/developer-docs/latest/getting-started/python.html 