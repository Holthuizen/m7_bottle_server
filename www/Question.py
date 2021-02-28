import json
import requests as request
#interface 
class Question:
    def __init__(self):
        self.api_url = "http://localhost:1337"

    def all(self):
        r = request.get(self.api_url + "/questions")
        return r.json()
    
    def validation(self,json_responce): 
        for obj in json_responce: 
            if not obj["Tilte"] and obj["description"] and obj["published_at"]: 
                return False
        return True

    #CRUD
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

    def read(self):
        endpoint = self.api_url + "/questions"
        #token = f'Bearer {jwt}'
        headers = {'Content-Type': 'application/json'}
        r = request.get(endpoint, headers=headers)
        return r

    def update(self): 
        pass
    def delete(self):
        pass

