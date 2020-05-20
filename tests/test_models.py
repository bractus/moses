import unittest
import os
import json
from app import create_app, db
from client import MosesClient


class BucketlistTestCase(unittest.TestCase):
    """This class represents the bucketlist test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.m_client = MosesClient()
        self.app = create_app(config_name="testing")
        # self.client = self.app.test_client
        self.mlmodel = {'name': 'SKLearn SVM',
                        'description': 'Just another model'}
        path = os.getcwd()
        self.model = open(path+'/save_models/save.pickle', 'rb')
        self.data = {}
        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.session.close()
            db.drop_all()
            db.create_all()

    def register_user(self, email="user@test.com", password="test1234"):
        user_data = {
            'email': email,
            'password': password
        }
        return self.m_client.register(user_data)

    def login_user(self, email="user@test.com", password="test1234"):
        user_data = {
            'email': email,
            'password': password
        }
        self.register_user()
        return self.m_client.login(user_data)

    def test_model_creation(self):
        """Test API can create a model (POST request)"""
        self.register_user()
        self.login_user()

        res = self.m_client.create(data=self.mlmodel,
                                   model=self.model)
        self.assertEqual(res['status_code'], 201)
        self.assertIn('SKLearn SVM', res['name'])

    # def test_api_can_get_all_models(self):
    #     """Test API can get a model (GET request)."""
    #     self.register_user()
    #     self.login_user()

    #     res = self.m_client.create(data=self.mlmodel,
    #                                model=self.model)
    #     self.assertEqual(res['status_code'], 201)
    #     res = self.m_client.list_all()
    #     self.assertEqual(res['status_code'], 200)
    #     self.assertIn('SKLearn SVM', res['data'][0]['name'])

    # def test_api_can_get_model_by_id(self):
    #     """Test API can get a single model by using it's id."""
    #     self.register_user()
    #     self.login_user()

    #     rv = self.m_client.create(data=self.mlmodel,
    #                               model=self.model)
    #     self.assertEqual(rv['status_code'], 201)

    #     result = self.m_client.list_by_id(rv['id'])
    #     self.assertEqual(result['status_code'], 200)
    #     self.assertIn('SKLearn SVM', result['data'][0]['name'])

    # def test_api_predict(self):
    #     self.register_user()
    #     self.login_user()

    #     rv = self.m_client.create(data=self.mlmodel,
    #                               model=self.model)
    #     self.assertEqual(rv['status_code'], 201)

    #     result = self.m_client.predict(rv['id'], self.data)
    #     self.assertEqual(result['status_code'], 200)
        # self.assertIn(data1, result['data'][0]['name'])
 
    # def test_model_deletion(self):
    #     """Test API can delete an existing bucketlist. (DELETE request)."""
    #     self.register_user()
    #     result = self.login_user()
    #     access_token = json.loads(result.data.decode())['access_token']

    #     rv = self.client().post(
    #         '/bucketlists/',
    #         headers=dict(Authorization="Bearer " + access_token),
    #         data={'name': 'Eat, pray and love'})
    #     self.assertEqual(rv.status_code, 201)
    #     # get the bucketlist in json
    #     results = json.loads(rv.data.decode())
    #     res = self.client().delete(
    #         '/bucketlists/{}'.format(results['id']),
    #         headers=dict(Authorization="Bearer " + access_token),)
    #     self.assertEqual(res.status_code, 200)
    #     # Test to see if it exists, should return a 404
    #     result = self.client().get(
    #         '/bucketlists/1',
    #         headers=dict(Authorization="Bearer " + access_token))
    #     self.assertEqual(result.status_code, 404)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
