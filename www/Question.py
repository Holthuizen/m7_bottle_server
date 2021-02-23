import json
import requests as request
#interface 
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

