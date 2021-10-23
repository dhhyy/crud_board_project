from unittest import mock
import bcrypt
import json
import jwt

from datetime      import date, datetime
from django.test   import TestCase, Client
from django.http   import response
from boards.models import Board, Category, Tag
from users.models  import User
from my_settings   import SECRET_KEY, algorithm
from unittest.mock import patch, Mock
# from freezegun     import freeze_time

class PostingTest(TestCase):
    
    def setUp(self):
        self.client  = Client()
        
        password          = '1234'
        hashed_password   = bcrypt.hashpw(password.encode('UTF-8'), bcrypt.gensalt()).decode('UTF-8')
        
        Category.objects.create(
            id   = 1,
            name = 'category_test'
        )
        
        Tag.objects.create(
            id       = 1,
            name     = "test",
            category = Category.objects.get(id=1)
        )
        User.objects.create(
            email    = 'test1@test.com',
            password = hashed_password,
            name     = 'runningman'
        )
        
        Board.objects.create(
            title    = 'testing_title',
            content  = 'testing_content,',
            writer   = User.objects.get(id=1),
            password = hashed_password,
            tag      = Tag.objects.get(id=1)
        )

    def tearDown(self):
        User.objects.all().delete()
        Board.objects.all().delete()
        Tag.objects.all().delete()
        Category.objects.all().delete()
        
    def test_success_posting(self):

        signin_user = {
            "email"    : "test1@test.com",
            "password" : "1234"
        }

        signin_response = self.client.post('/users/signin', json.dumps(signin_user), content_type='application/json')
        header = {'HTTP_Authorization' : signin_response.json()['access_token']}
        
        data   = {
            "title"    : "testing_post_1",
            "content"  : "testing_content",
            "password" : "1234",
            "writer"   : 1,
            "tag"      : 1
        }
        
        response = self.client.post('/boards/post', json.dumps(data), content_type='application/json', **header)
        self.assertEqual(response.status_code, 200)
        
    def test_fail_not_input_data(self):
        
        signin_user = {
            "email"    : "test1@test.com",
            "password" : "1234"
        }

        signin_response = self.client.post('/users/signin', json.dumps(signin_user), content_type='application/json')

        header = {'HTTP_Authorization' : signin_response.json()['access_token']}
        
        data   = {
            "password" : "1234",
            "writer"   : 1,
            "tag"      : 1
        }
        
        response = self.client.post('/boards/post', json.dumps(data), content_type='application/json', **header)
        self.assertEqual(response.status_code, 400)
        
    def test_fail_same_title_posting(self):
    
        signin_user = {
            "email"    : "test1@test.com",
            "password" : "1234"
        }

        signin_response = self.client.post('/users/signin', json.dumps(signin_user), content_type='application/json')
        header = {'HTTP_Authorization' : signin_response.json()['access_token']}
        
        data   = {
            "title"    : 'testing_title',
            "content"  : "testing_content",
            "password" : "1234",
            "writer"   : 1,
            "tag"      : 1
        }
        
        response = self.client.post('/boards/post', json.dumps(data), content_type='application/json', **header)
        self.assertEqual(response.status_code, 400)
        
    def test_fail_keyerror_posting(self):
    
        signin_user = {
            "email"    : "test1@test.com",
            "password" : "1234"
        }

        signin_response = self.client.post('/users/signin', json.dumps(signin_user), content_type='application/json')

        header = {'HTTP_Authorization' : signin_response.json()['access_token']}
        
        data   = {
            "title1"   : "testing_post",
            "content"  : "testing_content",
            "password" : "1234",
            "writer"   : 1,
            "tag"      : 1
        }
        
        response = self.client.post('/boards/post', json.dumps(data), content_type='application/json', **header)
        self.assertEqual(response.status_code, 400)