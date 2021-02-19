
import bottle 
from bottle import route, run, get, post, redirect, template, SimpleTemplate
import requests as request 
import json

#security 
import secrets
import hashlib


'''setup ---------------------------------------------------------------------''' 
CONFIG = None
with open('config.txt') as json_file:
    CONFIG = json.load(json_file)
     
#base url
SERVER_URL = f"http://{CONFIG['host']}:{CONFIG['port']}"
''' end setup -----------------------------------------------------------------''' 





def auth():
    api_url = "http://localhost:1337"
    r = request.post(api_url + "/auth/local",
    data=json.dumps({
        'identifier': "Student1",
        'password': "test1234"
    }),
    headers={
        'Content-Type': 'application/json'
    })
    return r


@get('/')
def index():
    return "home sweet home"

'''/questions?subject&test'''
@get('/questions')
def index():
    return "list all open questions"

'''LOGIN ---------------------------------------------------------------------''' 
#login view
@get('/login')
def login():
    return template('login')


# login logic
@post('/login')
def login():
    postdata = bottle.request.body.read()
    username = bottle.request.forms.get("username")
    pw = bottle.request.forms.get("password")

    #send auth request. 
    r = auth()
    data = r.json()
    status = r.status_code
    if data['jwt'] and status == 200: 
        print("Role: " , data['user']['role']['type'])

        #store token in cookie.
        """
        limit cookie to / paths. 
        cookies are signed with server secret
        """    
        cookie_config = dict(path='/', httponly=True, samesite="strict", secret= CONFIG['secret'].encode())
        bottle.response.set_cookie("token",data['jwt'],**cookie_config)
        bottle.response.set_cookie("user",data['user']['email'], **cookie_config)
        
        return "logged in"
        # return redirect(server_url + "/admin")
'''LOGIN ---------------------------------------------------------------------''' 



class Question:
    def __init__(self):
        self.api_url = "http://localhost:1337"

    def all(self):
        r = request.get(self.api_url + "/questions")
        return r.json()

    def create(self, jwt, params):
        token = f'Bearer {jwt}'
        endpoint = self.api_url + "/questions"
        data = json.dumps({
            'Title': params["title"],
            'description': params["description"],
            'question': params["question"]
        })
        headers = {'Content-Type': 'application/json', 'Authorization': token}
        r = request.post(endpoint,data=data, headers=headers)
        return r

#view
@get('/question/new')
def question_forum():
    #auth
    #read cookies
    token = bottle.request.get_cookie("token", secret=CONFIG['secret'].encode())
    if not (token): 
        print("no token pressend")
        return redirect(SERVER_URL + "/login")

    return template('question_form')

#logic
@post("/question/new")
def submit_question(): 

    #auth
    #read cookies
    token = bottle.request.get_cookie("token", secret=CONFIG['secret'].encode())
    if not (token): 
        print("no token pressend")
        return redirect(SERVER_URL + "/login")
    #read form data
    data = {}
    data['title'] = bottle.request.forms.get("title")
    data['description'] = bottle.request.forms.get("description")
    data['question'] = bottle.request.forms.get("question")

    #validation..

    #send data to strapi 
    q = Question()
    res = q.create(token,data)
    return res.json()



'''START SERVER---------------------------------------------------------------------''' 
run(host='localhost', port=CONFIG['port'], debug=True, reload=True)


#https://strapi.io/documentation/developer-docs/latest/getting-started/python.html 