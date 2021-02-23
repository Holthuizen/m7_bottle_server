
import bottle, json
import requests as request
class Authenticate: 
    def __init__(self,secret,base_url): 
        self.api_url = "http://localhost:1337/auth/local"
        self.config = dict(path='/', httponly=True, samesite="strict", secret=secret)
        self.secret = secret

    def login(self,username,pw): 
        if not (username and pw): 
            return False
        #auth request
        headers = {'Content-Type': 'application/json'}
        data = json.dumps({'identifier':username, 'password':pw})
        print(data)
        #return data, headers
        r = request.post(self.api_url, data=data, headers=headers)
        print(r.json())

        if r.status_code != 200: 
            return False

        jwt = r.json()['jwt']
        bottle.response.set_cookie("token",jwt,**self.config)
        return True

    #check if cookie with jwt is set
    def auth(self): 
        return bottle.request.get_cookie('token',secret=self.secret) or False


    def logout(self): 
        if bottle.request.get_cookie('token',secret=self.secret): 
            bottle.response.delete_cookie("token",path='/',secret=self.secret)
            return True
        return False       
