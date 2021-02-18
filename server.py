from bottle import route, run, get, post, request, response, redirect, template, SimpleTemplate, TEMPLATE_PATH
#security 
import secrets
import hashlib
import json

'''----- setup ------ ''' 
CONFIG = None
with open('config.txt') as json_file:
    CONFIG = json.load(json_file)
     
#base url
SERVER_URL = f"http://{CONFIG['host']}:{CONFIG['port']}"
print(SERVER_URL)

'''----- end setup ------ ''' 

@get('/')
def index():
    return "home sweet home"


''' START SERVER '''
run(host='localhost', port=CONFIG['port'], debug=True, reload=True)