import requests


class MosesClient:

    def __init__(self):
        #  TODO Carregar de um arquivo
        self.ADDRESS = 'http://127.0.0.1:5000'
        self.headers = None
        self.user_id = None

    def register(self, user_data):
        r = requests.post(self.ADDRESS + '/auth/register', data=user_data)
        return r.json()

    def login(self, user_data):
        r = requests.post(self.ADDRESS + '/auth/login', data=user_data)
        r = r.json()
        if r.get('access_token', None):
            self.headers = r['access_token']
            self.headers = {'Authorization':  "Bearer "+self.headers}
            return self.headers
        return r

    def create(self, data, model):
        # TODO se for instância de str ou de file
        if type(model) is str:
            files = {'file': open(model, 'rb')}
        else:
            files = {'file': model}  # TODO instanceof

        r = requests.post(self.ADDRESS + '/models/', data=data,
                          files=files, headers=self.headers)

        return r.json()

    def list_all(self):
        r = requests.get(self.ADDRESS + '/models/', headers=self.headers)
        return r.json()

    def list_by_id(self, id):
        r = requests.get(self.ADDRESS + '/models/', data={'id': id},
                         headers=self.headers)
        return r.json()

    def predict(self, id, data):
        pred_data = {
            'id': id,
            'data': data
        }
        r = requests.get(self.ADDRESS + '/predict/', data=pred_data,
                         headers=self.headers)
        return r.json()

    def delete(self, id):
        pass
