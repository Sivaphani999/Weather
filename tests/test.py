import unittest
from weatherapp import app
from pymongo import MongoClient


class TestCases(unittest.TestCase):

    def test_1_login(self):
        self.tester = app.test_client(self)
        response = self.tester.get('/login')
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    def test_2_signup(self):
        self.tester = app.test_client(self)
        response = self.tester.get('/signup')
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)

    def test_3_signup_post(self):
        self.tester = app.test_client(self)
        response = self.tester.post('/signup', data={
            'username': 'siva',
            'password': '1234',
            'ConfirmPassword': '1234'
        })
        status_code = response.status_code
        self.assertEqual(status_code, 200)

    def test_4_signup_db(self):
        self.tester = app.test_client(self)
        client = MongoClient('mongodb://127.0.0.1:27017')
        db = client['login']
        collection = db['login_coln']
        before_post_req = collection.count_documents({})
        response = self.tester.post('/signup', data={
            'username': 'phani',
            'password': '1234',
            'ConfirmPassword': '1234'
        })
        after_post_req = collection.count_documents({})
        self.assertEqual(before_post_req+1, after_post_req)

    def test_5_signup_db1(self):
        self.tester = app.test_client(self)
        client = MongoClient('mongodb://127.0.0.1:27017')
        db = client['login']
        collection = db['login_coln']
        before_post_req = collection.count_documents({})
        response = self.tester.post('/signup', data={
            'username': 'siva',
            'password': '1234',
            'ConfirmPassword': '1234'
        })
        after_post_req = collection.count_documents({})
        self.assertEqual(before_post_req, after_post_req)

    def test_6_login(self):
        self.tester = app.test_client(self)
        response = self.tester.post('/login', data={
            'username': 'phani',
            'password': '1234'
        })
        status_code = response.status_code
        self.assertEqual(status_code, 200)

    def test_7_weather(self):
        self.tester = app.test_client(self)
        response = self.tester.post('/weather', data={
            'city': 'guntur'
        })
        status_code = response.status_code
        self.assertEqual(status_code, 200)


if __name__ == '__main__':
    unittest.main()
